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
        deployment_name = os.getenv("DEPLOYMENT_NAME")
        print("Azure OpenAI client initialized successfully")
    except Exception as e:
        print(f"Warning: Failed to initialize Azure OpenAI client: {e}")
        AZURE_AVAILABLE = False
        client = None
else:
    print("Azure OpenAI credentials not available - using fallback responses")

def log_qna(question: str, answer: str):
    """Append a new question-answer pair to a JSON file."""
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "answer": answer
    }

    # Load existing data if available
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    data.append(record)

    # Ensure directory exists
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Initialize components only if Azure is available
qa_chain = None
if AZURE_AVAILABLE and os.path.exists(INDEX_PATH):
    try:
        # Load Vector Store 
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever()

        llm = AzureChatOpenAI(
            azure_deployment=os.getenv("DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_API_KEY"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_version=os.getenv("AZURE_API_VERSION"),
            temperature=0,
        )

        template = """
You are a medical assistant explaining COVID-19 reinfection risk using research evidence.

Patient details (from the system):
- Age and demographics are included in the question
- Vaccine history and conditions are included in the question

Scientific evidence:
{context}

TASK:
1. Start with an empathetic statement to the patient.
2. Clearly state the risk level for reinfection (Low / Moderate / High).
3. In 3-5 sentences, explain the risk factors and patterns from the evidence
   that match the patient's profile (e.g., age, vaccine, conditions).
Only use the given scientific evidence and do not add unsupported information.

Format your response exactly like this:
Based on the research, the risk level is **[Risk Level]**.

According to the evidence, [explain the specific findings that apply to this patient's profile, mentioning relevant factors like age, vaccination status, underlying conditions, etc.].

Question:
{question}
"""

        prompt = PromptTemplate(template=template, input_variables=["context", "question"])

        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt}
        )
    except Exception as e:
        print(f"Warning: Failed to initialize RAG components: {e}")

def build_query(patient: dict) -> str:
    """
    Convert patient dictionary into a query string for retrieval.
    """
    age = patient.get('Age', patient.get('age', ''))
    doses = patient.get('Doses_Received', patient.get('doses', ''))
    vaccine = patient.get('Vaccine_Type', patient.get('vaccine', ''))
    conditions = patient.get('Preexisting_Condition', patient.get('conditions', []))
    
    if isinstance(conditions, str):
        conditions = [conditions]
    elif not isinstance(conditions, list):
        conditions = []
    
    parts = [
        f"age {age}",
        f"{doses} doses {vaccine}",
        " ".join(conditions)
    ]
    return f"COVID reinfection risk factors for {' '.join(parts)}"

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
        
        fallback_response = f"""[ RAG Medical Literature ]
I understand you have questions about your risk of getting COVID-19 again, and it's smart to stay informed.

Based on general medical knowledge, the risk level is **Moderate**.

According to general medical principles, patients aged {age} with {conditions} condition(s) and {vaccine_status} vaccination status may have varying reinfection risks. Factors like previous infection severity ({severity}), vaccination history, underlying health conditions, and time since last infection all contribute to individual risk assessment. For comprehensive analysis, please consult healthcare professionals who can access current research and provide personalized medical advice.

Note: This is a general response as the AI-powered analysis system requires Azure OpenAI configuration."""
        
        query = build_query(patient)
        log_qna(query, fallback_response)
        return fallback_response.strip()
    
    try:
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
