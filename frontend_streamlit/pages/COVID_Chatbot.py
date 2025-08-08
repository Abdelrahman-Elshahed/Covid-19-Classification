from fastapi import Request
import streamlit as st
import sys
import os
import json
import requests

# Add the parent directory to sys.path to import modules from RagModule
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from RagModule.scripts.rag_pipeline import log_qna
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import AzureChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Set page configuration
st.set_page_config(
    page_title="COVID-19 Knowledge Chatbot",
    page_icon="🔬",
    layout="wide",
)

# Load environment variables
load_dotenv()

# Paths
INDEX_PATH = os.path.join(os.path.dirname(__file__), "../../RagModule/vectorstore/faiss_pubmed")

# Initialize the session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize RAG components
@st.cache_resource
def load_rag_components():
    """Load RAG components (vectorstore, LLM, retriever)"""
    try:
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
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # Limit to top 3 results
        
        # Define Prompt Template for chatbot
        template = """
        You are a medical assistant answering questions about COVID-19 using scientific research evidence.
        
        Answer the user's question based ONLY on the scientific evidence provided below.
        Be concise and accurate in your response.
        If the evidence doesn't contain information to answer the question, admit that you don't know.
        
        Scientific evidence:
        {context}
        
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
        
        return qa_chain
    except Exception as e:
        st.error(f"Error loading RAG components: {str(e)}")
        return None

# Query function
def query_rag(question):
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"question": question},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status() # Raise an error for bad responses
        return response.json()["response"]
    except requests.Timeout:
        return "Request timeout. Please try again."
    except requests.RequestException as e:
        return f"Connection error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Display title and description
st.title("COVID-19 Research Chatbot")
st.markdown("""
This chatbot uses a Retrieval-Augmented Generation (RAG) system to answer questions about COVID-19 
based on scientific literature from PubMed abstracts. Ask any question related to COVID-19, such as
transmission, symptoms, vaccination, reinfection risk, or treatments.
""")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new message
if prompt := st.chat_input("Ask a question about COVID-19..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response with a spinner
    with st.chat_message("assistant"):
        with st.spinner("Searching medical literature..."):
            response = query_rag(prompt)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with information
st.sidebar.title("About this Chatbot")
st.sidebar.markdown("""
### Data Sources
- PubMed abstracts related to COVID-19

### Technologies
- Langchain
- FAISS vector database
- Azure OpenAI

### Example Questions
- How effective are vaccines against new variants?
- How does vaccination impact reinfection rates?
- What is the likelihood of reinfection after recovery?
- How does age affect COVID-19 outcomes?
- What are the common symptoms of Long COVID?
""")

# Clear chat button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()