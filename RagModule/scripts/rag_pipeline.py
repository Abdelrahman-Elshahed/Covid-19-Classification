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

# Validate required environment variables
REQUIRED_ENV_VARS = [
    "AZURE_API_KEY",
    "AZURE_API_VERSION",
    "AZURE_ENDPOINT",
    "DEPLOYMENT_NAME"
]
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Validate vectorstore exists
if not os.path.exists(INDEX_PATH):
    raise FileNotFoundError(f"Vector index not found at {INDEX_PATH}. Please generate it first.")

# Initialize Azure LLM
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("DEPLOYMENT_NAME"),
    api_key=os.getenv("AZURE_API_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version=os.getenv("AZURE_API_VERSION"),
    temperature=0,
)

# Initialize Vector Store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # Limit to top 3 results

# Define Prompt Template
template = """
You are a medical assistant explaining COVID-19 reinfection risk using research evidence.

Patient details:
- Age, Gender, Vaccine Type, Doses Received, Preexisting Condition, COVID Strain, Symptoms, Severity, Hospitalization Status, ICU Admission, Ventilator Support, BMI, Smoking Status, last infection date and last dose date are included in the question
- Use the patient's profile to tailor the explanation
Scientific evidence:
{context}

TASK:
1. Start with an empathetic statement.
2. State the risk level (Low/Moderate/High).
3. In 3-5 sentences, explain risk factors from evidence matching the patient's profile.
Only use the given scientific evidence.

Format response exactly:
Based on the research, the risk level is **[Risk Level]**.

According to the evidence, [explanation with patient-specific factors].

Question:
{question}
"""
prompt = PromptTemplate(template=template, input_variables=["context", "question"])

# Initialize QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt}
)

def log_qna(question: str, answer: str):
    """Log Q&A to JSON file"""
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "answer": answer
    }
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    
    data.append(record)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def build_query(patient: dict) -> str:
    """Convert ALL relevant patient data into a detailed query"""
    base_info = (
        f"Patient: {patient.get('Age')} years, "
        f"{patient.get('Gender')}, "
        f"Vaccine: {patient.get('Vaccine_Type')} ({patient.get('Doses_Received')} doses), "
        f"Conditions: {patient.get('Preexisting_Condition')}, "
        f"Strain: {patient.get('COVID_Strain')}, "
        f"Symptoms: {patient.get('Symptoms')} ({patient.get('Severity')})"
    )
    
    clinical_details = (
        f"Hospitalized: {patient.get('Hospitalized')}, "
        f"ICU: {patient.get('ICU_Admission')}, "
        f"Ventilator: {patient.get('Ventilator_Support')}, "
        f"BMI: {patient.get('BMI')}, "
        f"Smoking: {patient.get('Smoking_Status')}"
    )
    
    time_factors = (
        f"Last infection: {patient.get('Date_of_Infection')}, "
        f"Last dose: {patient.get('Date_of_Last_Dose')}"
    )
    
    return (
        f"COVID-19 reinfection risk assessment considering:\n"
        f"1. {base_info}\n"
        f"2. {clinical_details}\n"
        f"3. {time_factors}"
    )

def generate_explanation(patient: dict) -> str:
    """Generate explanation using RAG system only"""
    query = build_query(patient)
    try:
        response = qa_chain.invoke(query)["result"]
        formatted_response = f"[ RAG Medical Literature ]\n{response}"
        log_qna(query, formatted_response)
        return formatted_response
    except Exception as e:
        error_msg = f"RAG system error: {str(e)}"
        log_qna(query, error_msg)
        return f"[ RAG Medical Literature ]\n{error_msg}"

# Function to generate chat response using RAG system secondary to the main function & second page in COVID_Chatbot.py (streamlit app)
def generate_chat_response(question: str) -> str:
    if not hasattr(generate_chat_response, "qa_chain"):
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        
        llm = AzureChatOpenAI(
            azure_deployment=os.getenv("DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_API_KEY"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_version=os.getenv("AZURE_API_VERSION"),
            temperature=0
        )
        
        prompt_template = """
        You are a medical assistant answering questions about COVID-19 using scientific research evidence.
        
        Answer the user's question based ONLY on the scientific evidence provided below.
        Be concise and accurate in your response.
        If the evidence doesn't contain information to answer the question, admit that you don't know.
        
        Scientific evidence:
        {context}
        
        Question:
        {question}
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        generate_chat_response.qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": prompt}
        )
    
    try:
        result = generate_chat_response.qa_chain.invoke(question)["result"]
        log_qna(question, result)
        return result
    except Exception as e:
        return f"Error generating response: {str(e)}"
    
def generate_ml_aware_response(patient: dict, ml_prediction: str = None) -> str:
    """Generate explanation combining ML prediction and RAG evidence"""
    query_text = build_query(patient)
    
    # Provide a default value if ml_prediction is None
    if ml_prediction is None:
        ml_prediction = "Unknown"
    
    try:
        # Directly retrieve relevant documents
        docs = retriever.invoke(query_text)
        
        # Combine document content into context
        context_text = "\n\n".join([doc.page_content for doc in docs])
        
        # Create the complete prompt as a string with all variables directly included
        ml_aware_prompt = f"""
You are a medical assistant explaining COVID-19 reinfection risk using research evidence.
The ML model has predicted: {ml_prediction} risk for this patient.

Patient details:
{query_text}
- Age, Gender, Vaccine Type, Doses Received, Preexisting Condition, COVID Strain, Symptoms, Severity, Hospitalization Status, ICU Admission, Ventilator Support, BMI, Smoking Status, last infection date and last dose date are included in the question
- Use the patient's profile to tailor the explanation

Scientific evidence:
{context_text}

TASK:
1. Start with an empathetic statement.
2. State the risk level (Low/Moderate/High).
3. In 3-5 sentences, explain risk factors from evidence matching the patient's profile.
Only use the given scientific evidence.

Format response exactly:
Based on the research, the risk level is **[Risk Level]**.
ML Prediction: {ml_prediction} risk.
According to the evidence, [explanation with patient-specific factors].
"""
        
        # Call the LLM directly without using RetrievalQA
        response = llm.invoke(ml_aware_prompt)
        
        # Format the response
        if hasattr(response, 'content'):
            result = response.content
        else:
            result = str(response)
            
        formatted_response = f"[ Integrated Analysis ]\n{result}"
        log_qna(f"ML: {ml_prediction} - {query_text}", formatted_response)
        return formatted_response
        
    except Exception as e:
        error_msg = f"Integration error: {str(e)}"
        log_qna(query_text, error_msg)
        return f"[ Integrated Analysis ]\n{error_msg}"