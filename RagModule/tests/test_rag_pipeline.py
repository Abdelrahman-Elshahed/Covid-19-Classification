from scripts.rag_pipeline import generate_explanation

patient = {
  "Age": 0,
  "Gender": "string",
  "Region": "string",
  "Preexisting_Condition": "string",
  "Date_of_Infection": "2025-08-06T11:37:20.524Z",
  "COVID_Strain": "string",
  "Symptoms": "string",
  "Severity": "string",
  "Hospitalized": "string",
  "Hospital_Admission_Date": "2025-08-06T11:37:20.524Z",
  "Hospital_Discharge_Date": "2025-08-06T11:37:20.524Z",
  "ICU_Admission": "string",
  "Ventilator_Support": "string",
  "Recovered": "string",
  "Date_of_Recovery": "2025-08-06T11:37:20.524Z",
  "Date_of_Reinfection": "2025-08-06T11:37:20.524Z",
  "Vaccination_Status": "string",
  "Vaccine_Type": "string",
  "Doses_Received": 0,
  "Date_of_Last_Dose": "2025-08-06T11:37:20.524Z",
  "Long_COVID_Symptoms": "string",
  "Occupation": "string",
  "Smoking_Status": "string",
  "BMI": 0,
  "Recovery_Classification": "string"
}

print(generate_explanation(patient))
