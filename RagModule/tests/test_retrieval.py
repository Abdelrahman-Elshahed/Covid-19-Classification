from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

INDEX_PATH = os.path.join(os.path.dirname(__file__), "../vectorstore/faiss_pubmed")

def test_retrieval(query: str):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

    results = vectorstore.similarity_search(query, k=3)
    for r in results:
        print("---")
        print(r.metadata["pmid"], ":", r.page_content[:300])

if __name__ == "__main__":
    query = "COVID reinfection risk for older patients after vaccination"
    test_retrieval(query)
