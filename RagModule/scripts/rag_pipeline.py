import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


load_dotenv()

LOG_PATH = os.path.join(os.path.dirname(__file__), "../data/qna_history.json")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "../vectorstore/faiss_pubmed")

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

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Load Vector Store 
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)

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

Question:
{question}
"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt}
)

def build_query(patient: dict) -> str:
    """
    Convert patient dictionary into a query string for retrieval.
    """
    parts = [
        f"age {patient.get('age', '')}",
        f"{patient.get('doses', '')} doses {patient.get('vaccine', '')}",
        " ".join(patient.get('conditions', []))
    ]
    return f"COVID reinfection risk factors for {' '.join(parts)}"

def generate_explanation(patient: dict) -> str:
    """
    Generate a scientific explanation for reinfection risk.
    Logs the question and answer in a JSON file.
    """
    query = build_query(patient)
    response = qa_chain.run(query)

    log_qna(query, response)

    return response
