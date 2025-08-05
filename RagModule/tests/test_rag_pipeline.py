from scripts.rag_pipeline import generate_explanation

patient = {
    "age": 65,
    "vaccine": "Pfizer",
    "doses": 2,
    "conditions": ["diabetes", "hypertension"]
}

print(generate_explanation(patient))
