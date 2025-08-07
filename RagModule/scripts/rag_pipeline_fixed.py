import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

LOG_PATH = os.path.join(os.path.dirname(__file__), "../data/qna_history.json")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "../vectorstore/faiss_pubmed")

# Check if Azure credentials are available
AZURE_AVAILABLE = all([
    os.getenv("AZURE_API_KEY"),
    os.getenv("AZURE_API_VERSION"),
    os.getenv("AZURE_ENDPOINT"),
    os.getenv("DEPLOYMENT_NAME")
])

# Initialize Azure OpenAI client only if credentials are available
client = None
if AZURE_AVAILABLE:
    try:
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT")
        )
        print("Azure OpenAI client initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize Azure OpenAI client: {e}")
        AZURE_AVAILABLE = False
else:
    print("Azure OpenAI credentials not available. Using fallback responses.")

# Initialize the chain only if Azure OpenAI is available
qa_chain = None
if AZURE_AVAILABLE:
    try:
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Load FAISS vector store
        vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

        # Initialize Azure LLM
        llm = AzureChatOpenAI(
            deployment_name=os.getenv("DEPLOYMENT_NAME"),
            model_name="gpt-4",
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_key=os.getenv("AZURE_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            temperature=0.3
        )

        # Create the QA chain
        prompt_template = """
        You are a medical AI assistant specializing in COVID-19. Based on the following medical literature context, 
        provide a comprehensive analysis about COVID-19 reinfection risk, recovery patterns, and medical recommendations.

        Context: {context}

        Question: {question}

        Please provide a detailed, evidence-based response that includes:
        1. Risk assessment based on available research
        2. Relevant medical factors and considerations
        3. General recommendations (while noting that individual medical advice should come from healthcare professionals)

        Answer:
        """

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT}
        )
        print("QA chain initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize QA chain: {e}")
        qa_chain = None
        AZURE_AVAILABLE = False

def log_qna(question: str, answer: str):
    """Log questions and answers to a JSON file."""
    try:
        # Load existing data
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []

        # Add new Q&A
        entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer
        }
        history.append(entry)

        # Save back to file
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"Error logging Q&A: {e}")

def build_query(patient: dict) -> str:
    """
    Build a query for retrieving relevant medical literature about reinfection risk.
    """
    age = patient.get('Age', patient.get('age', 'unknown'))
    vaccine_status = patient.get('Vaccination_Status', 'unknown')
    conditions = patient.get('Preexisting_Condition', 'none')
    severity = patient.get('Severity', patient.get('Symptoms', 'unknown'))
    
    query = f"""
    What are the COVID-19 reinfection risks for a {age}-year-old patient with {conditions} preexisting conditions, 
    {vaccine_status} vaccination status, and {severity} symptom severity? 
    Include information about recovery patterns and vaccination effectiveness.
    """
    
    return query.strip()

def build_chat_query(patient: dict) -> str:
    """
    Build a query for the chat interface.
    If a direct question is provided, use it.
    Otherwise build a context-specific query.
    """
    # Check if there's a direct question in the patient object
    if "question" in patient and patient["question"]:
        return patient["question"]
    
    # If no direct question, build a query as usual
    return build_query(patient)

def generate_explanation(patient: dict) -> str:
    """
    Generate a scientific explanation for reinfection risk.
    Logs the question and answer in a JSON file.
    """
    if not AZURE_AVAILABLE or qa_chain is None:
        # Fallback response when Azure OpenAI is not available
        age = patient.get('Age', patient.get('age', 'unknown'))
        vaccine_status = patient.get('Vaccination_Status', 'unknown')
        conditions = patient.get('Preexisting_Condition', 'none')
        severity = patient.get('Severity', patient.get('Symptoms', 'unknown'))
        
        # If it's a direct question through the chat interface
        if "question" in patient:
            fallback_response = f"""[ RAG Medical Literature ]
I understand you're asking: "{patient['question']}"

Without access to the medical database, I can only provide general information. For accurate medical advice, please consult with healthcare professionals.

Based on general knowledge, questions about COVID-19 can involve symptoms, prevention strategies, treatment options, and risk factors. The specific context of your question would require access to current medical literature and research findings.
"""
            log_qna(patient["question"], fallback_response)
            return fallback_response.strip()
        
        # Original fallback for prediction context
        fallback_response = f"""[ RAG Medical Literature ]
I understand you have questions about your risk of getting COVID-19 again, and it's smart to stay informed.

Based on general medical knowledge, the risk level is **Moderate**.

According to general principles, patients aged {age} with {conditions} condition(s) and {vaccine_status} vaccination status may have varying reinfection risks. Factors like previous infection severity ({severity}), vaccination history, underlying health conditions, and time since last infection all contribute to individual risk assessment. For comprehensive analysis, please consult healthcare professionals who can access current research and provide personalized medical advice.

Note: This is a general response as the AI-powered analysis system requires Azure OpenAI configuration."""
        
        query = build_query(patient)
        log_qna(query, fallback_response)
        return fallback_response.strip()
    
    try:
        # Determine if this is a direct question or a patient context
        if "question" in patient:
            query = patient["question"]
        else:
            query = build_query(patient)
            
        response = qa_chain.invoke(query)["result"]
        
        # Format the response with RAG Medical Literature header
        formatted_response = f"[ RAG Medical Literature ]\n{response}"
        
        log_qna(query, formatted_response)
        return formatted_response
    except Exception as e:
        error_response = f"[ RAG Medical Literature ]\nSorry, I'm unable to provide a detailed analysis at the moment due to a technical issue: {str(e)}"
        log_qna(build_query(patient), error_response)
        return error_response