from fastapi import FastAPI
from typing import List
import sys
import os
from app.schemas import PatientFeatures
from app.model_interface import get_prediction

#This line ensures the parent directory is in the path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RagModule.scripts.rag_pipeline import generate_explanation

app = FastAPI(
    title="Reinfection Prediction API",
    description="API for predicting reinfection based on patient features",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {"message": "COVID Reinfection Prediction API"}

@app.post("/predict")
def predict(data: List[PatientFeatures]):
    try:
        features = list(data)
        prediction = get_prediction(features)
        
        description = generate_explanation(features[0])
        
        return {"reinfection_prediction": prediction, "description": description}
    except Exception as e:
        return {"error": str(e)}