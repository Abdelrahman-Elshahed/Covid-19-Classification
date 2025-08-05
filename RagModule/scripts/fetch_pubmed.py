from Bio import Entrez
import pandas as pd
import os

Entrez.email = "zeyadabdelwahab684@gmail.com"

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/pubmed_abstracts.csv")

def fetch_pubmed(query, max_results=30):
    """Fetch abstracts from PubMed for a specific query."""
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    id_list = record["IdList"]
    
    abstracts = []
    for pmid in id_list:
        fetch_handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
        text = fetch_handle.read().replace("\n", " ").strip() #Removes newlines (\n) and trims whitespace
        fetch_handle.close()
        abstracts.append({"pmid": pmid, "text": text})
    return abstracts

if __name__ == "__main__":
    topics = [
        "COVID reinfection risk",
        "COVID vaccine effectiveness",
        "COVID recovery predictors",
        "Long COVID & Post-Acute Sequelae"
    ]

    all_abs = []
    for topic in topics:
        print(f"Fetching PubMed abstracts for: {topic}")
        all_abs.extend(fetch_pubmed(topic, max_results=100))

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    pd.DataFrame(all_abs).to_csv(DATA_PATH, index=False)
    print(f"Saved abstracts to {DATA_PATH}")
