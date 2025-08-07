from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import sys
import os
from app.schemas import PatientFeatures
from app.model_interface import get_prediction

#This line ensures the parent directory is in the path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from RagModule.scripts.rag_pipeline import generate_explanation
    RAG_AVAILABLE = True
except Exception as e:
    print(f"Warning: RAG module not available: {e}")
    RAG_AVAILABLE = False
    
    def generate_explanation(patient_data):
        return "Detailed explanation service is currently unavailable. Please consult healthcare professionals for personalized risk assessment."

app = FastAPI(
    title="Reinfection Prediction API",
    description="API for predicting reinfection based on patient features",
    version="1.0.0"
)

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
        "rag_available": RAG_AVAILABLE,
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "prediction_service": "available",
        "explanation_service": "available" if RAG_AVAILABLE else "limited"
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
        
        print(f"Received data: {data}")
        print(f"Processing {len(data)} features")
        
        # The validation and field mapping is now handled in the PatientFeatures model
        prediction = get_prediction(data)
        print(f"Prediction result: {prediction}")
        
        # Use the first patient's data for explanation
        first_patient_dict = data[0].model_dump() if hasattr(data[0], 'model_dump') else data[0].dict()
        description = generate_explanation(first_patient_dict)
        print(f"Description: {description}")
        
        result = {
            "reinfection_prediction": prediction, 
            "description": description,
            "rag_service_used": RAG_AVAILABLE
        }
        print(f"Returning result: {result}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in prediction: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")