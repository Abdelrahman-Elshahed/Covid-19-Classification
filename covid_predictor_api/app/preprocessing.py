import pandas as pd
import pickle
from  app.schemas import Patient_features
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent

MODEL_DIR = CURRENT_DIR.parent / "model"

with open(MODEL_DIR / "scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open(MODEL_DIR / "encoders.pkl", "rb") as f:
    encoders = pickle.load(f)

# Preprocessing the input data to match the model's expected format

def preprocess_input_data(patient_data: Patient_features):
    # df = pd.DataFrame([patient_data.dict()])
    
    # If patient_data is a list of Patient_features, convert each to dict
    if isinstance(patient_data, list):
        data_dicts = [p.dict() for p in patient_data]
    else:
        data_dicts = [patient_data.dict()]

    df = pd.DataFrame(data_dicts)
    
    # Ensure all columns are present
    expected_columns = list(scaler.feature_names_in_)
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0
            
    # Convert datetime fields to pandas datetime if they are not already
    date_cols = [col for col in df.columns if "Date" in col]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Basic preprocessing
    binary_cols = ['Hospitalized', 'ICU_Admission', 'Ventilator_Support', 'Recovered', 'Vaccination_Status']
    for col in binary_cols:
        df[col] = df[col].map({'Yes': 1, 'No': 0})

    df = df[(df['BMI'] >= 10) & (df['BMI'] <= 60)]
    df.reset_index(drop=True, inplace=True)

    # === New Features ===
    # 1. Recovery duration in days
    df["Recovery_Duration"] = (df["Date_of_Recovery"] - df["Date_of_Infection"]).dt.days

    # 2. Time to reinfection (post recovery)
    df["Time_to_Reinfection"] = (df["Date_of_Reinfection"] - df["Date_of_Recovery"]).dt.days
    df["Reinfected_Later"] = df["Time_to_Reinfection"].apply(lambda x: 1 if x > 0 else 0)

    # 3. Time between vaccination and infection
    df["Vaccine_to_Infection_Days"] = (df["Date_of_Infection"] - df["Date_of_Last_Dose"]).dt.days

    # 4. Hospital stay duration
    df["Hospital_Stay_Duration"] = (df["Hospital_Discharge_Date"] - df["Hospital_Admission_Date"]).dt.days
    # avoid negatives
    df["Hospital_Stay_Duration"] = df["Hospital_Stay_Duration"].apply(lambda x: x if x >= 0 else 0)  

    # 5. Is vaccinated & infected within 14 days?
    df["Infected_soon_after_vaccine"] = df["Vaccine_to_Infection_Days"].apply(lambda x: 1 if 0 <= x <= 14 else 0)

    # === Drop date columns to prepare for modeling ===
    df.drop(columns=[
        "Date_of_Infection", "Date_of_Recovery", "Date_of_Reinfection",
        "Hospital_Admission_Date", "Hospital_Discharge_Date", "Date_of_Last_Dose"
    ], inplace=True)

    # === Encoding categorical features ===
    for column in df.select_dtypes(include=['object']).columns:
        if column in encoders:
            df[column] = encoders[column].transform(df[column])
        else:
            df[column] = pd.factorize(df[column])[0]
    
    # === Scaling the features ===
    scaled_data = scaler.transform(df)

    return scaled_data