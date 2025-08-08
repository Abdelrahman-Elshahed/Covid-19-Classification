from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import sys
import os
from app.schemas import PatientFeatures
from app.model_interface import get_prediction
from pydantic import BaseModel
import requests 
#This line ensures the parent directory is in the path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RagModule.scripts.rag_pipeline import generate_explanation  # No try-except
from RagModule.scripts.rag_pipeline import generate_chat_response

app = FastAPI(
    title="Reinfection Prediction API",
    description="API for predicting reinfection based on patient features",
    version="1.0.0"
)
class ChatRequest(BaseModel):
    question: str

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "message": "COVID Reinfection Prediction API",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "services": ["prediction", "RAG_explanation"]
    }

@app.options("/predict")
def predict_options():
    """Handle CORS preflight requests for the predict endpoint"""
    return {"status": "ok"}

@app.post("/predict")
def predict(data: List[PatientFeatures]):
    try:
        if not data:
            raise HTTPException(status_code=400, detail="No patient data provided")
        
        # Get ML prediction
        prediction = get_prediction(data)     
        # Prepare patient data
        first_patient_dict = data[0].model_dump() if hasattr(data[0], 'model_dump') else data[0].dict()
        
        # Generate integrated explanation
        from RagModule.scripts.rag_pipeline import generate_ml_aware_response
        description = generate_ml_aware_response(
            patient=first_patient_dict,
            ml_prediction=str(prediction)
        )
        
        return {
            "reinfection_prediction": str(prediction), 
            "description": description,
            "services": ["prediction", "integrated_analysis"]
        }
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):  
    try:
        question = chat_request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        response = generate_chat_response(question)
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))