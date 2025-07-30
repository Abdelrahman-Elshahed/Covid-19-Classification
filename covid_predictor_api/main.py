from fastapi import FastAPI
from typing import List
from app.schemas import Patient_features
from app.model_interface import get_prediction

app = FastAPI(
    title="Reinfection Prediction API",
    description="API for predicting reinfection based on patient features",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {"message": "COVID Reinfection Prediction API"}

@app.post("/predict")
def predict(data: List[Patient_features]):
    try:
        prediction = get_prediction(data)
        features = list(data)
        prediction = get_prediction(features)
        
        description = []
        if data[0].Smoking_Status == 1:
            description.append("Smoker")
        else:
            description.append("Non-Smoker")
        if data[0].BMI > 30:
            description.append("High BMI")
        else:
            description.append("Normal BMI")
        if data[0].ICU_Admission == 1:
            description.append("ICU history")
        else:
            description.append("No ICU history")

        description = ", ".join(description) if description else "No critical risk indicators"
        return {"reinfection_prediction": prediction, "description": description}
    except Exception as e:
        return {"error": str(e)}