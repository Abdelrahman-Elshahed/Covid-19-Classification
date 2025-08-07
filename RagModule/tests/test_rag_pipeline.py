from scripts.rag_pipeline import generate_explanation

patient = {
    "Age": 45,
    "Gender": "Male",
    "Region": "Hovedstaden",
    "Preexisting_Condition": "Diabetes",
    "Date_of_Infection": "2023-04-15T00:00:00.000Z",
    "COVID_Strain": "Omicron",
    "Symptoms": "Moderate",
    "Severity": "Moderate",
    "Hospitalized": "Yes",
    "Hospital_Admission_Date": "2023-04-18T00:00:00.000Z",
    "Hospital_Discharge_Date": "2023-04-25T00:00:00.000Z",
    "ICU_Admission": "No",
    "Ventilator_Support": "No",
    "Recovered": "Yes",
    "Date_of_Recovery": "2023-05-10T00:00:00.000Z",
    "Date_of_Reinfection": "2024-05-10T00:00:00.000Z",
    "Vaccination_Status": "Yes",
    "Vaccine_Type": "Pfizer",
    "Doses_Received": 2,
    "Date_of_Last_Dose": "2023-01-15T00:00:00.000Z",
    "Long_COVID_Symptoms": "Fatigue",
    "Occupation": "Teacher",
    "Smoking_Status": "Former",
    "BMI": 25.3,
    "Recovery_Classification": "Typical Recovery"
}

print(generate_explanation(patient))
