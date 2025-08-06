import pandas as pd
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/pubmed_abstracts.csv")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "../vectorstore/faiss_pubmed")

def build_index():
    df = pd.read_csv(DATA_PATH)

    docs = [Document(page_content=row["text"], metadata={"pmid": row["pmid"]})
            for _, row in df.iterrows()]

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs(INDEX_PATH, exist_ok=True)
    vectorstore.save_local(INDEX_PATH)
    print(f"Vector store saved to {INDEX_PATH}")

if __name__ == "__main__":
    build_index()
