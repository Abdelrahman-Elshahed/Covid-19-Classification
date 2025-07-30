from pydantic import BaseModel
from datetime import datetime

class Patient_features(BaseModel):
    Age: int
    Gender: str
    Region: str
    Preexisting_Condition: str
    Date_of_Infection: datetime
    COVID_Strain: str
    Symptoms: str
    Severity: str
    Hospitalized: str
    Hospital_Admission_Date: datetime
    Hospital_Discharge_Date: datetime
    ICU_Admission: str
    Ventilator_Support: str
    Recovered: str
    Date_of_Recovery: datetime
    Date_of_Reinfection: datetime
    Vaccination_Status: str
    Vaccine_Type: str
    Doses_Received: int
    Date_of_Last_Dose: datetime
    Long_COVID_Symptoms: str
    Occupation: str
    Smoking_Status: str
    BMI: float
    Recovery_Classification: str