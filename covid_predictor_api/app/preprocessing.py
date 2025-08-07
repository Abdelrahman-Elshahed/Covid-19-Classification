import pandas as pd
import pickle
from  app.schemas import PatientFeatures
from pathlib import Path

def normalize_timezone(dt_series):
    """Convert datetime series to UTC timezone, handling both naive and aware datetimes"""
    if dt_series.dt.tz is None:
        # If timezone-naive, assume UTC
        return dt_series.dt.tz_localize('UTC')
    else:
        # If timezone-aware, convert to UTC
        return dt_series.dt.tz_convert('UTC')

CURRENT_DIR = Path(__file__).resolve().parent

MODEL_DIR = CURRENT_DIR.parent / "model"

with open(MODEL_DIR / "scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open(MODEL_DIR / "encoders.pkl", "rb") as f:
    encoders = pickle.load(f)

# Preprocessing the input data to match the model's expected format

def preprocess_input_data(patient_data: PatientFeatures):
    # If patient_data is a list of PatientFeatures, convert each to dict
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
            
    # Convert datetime fields to pandas datetime and normalize timezones
    date_cols = [col for col in df.columns if "Date" in col]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        # Ensure all datetimes are timezone-naive for consistent operations
        if hasattr(df[col].dtype, 'tz') and df[col].dt.tz is not None:
            df[col] = df[col].dt.tz_convert('UTC').dt.tz_localize(None)
        elif df[col].notna().any():
            # For timezone-naive datetimes, just ensure they're properly formatted
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Basic preprocessing
    binary_cols = ['Hospitalized', 'ICU_Admission', 'Ventilator_Support', 'Recovered', 'Vaccination_Status']
    for col in binary_cols:
        # Map known values, fill unknown values with -1
        df[col] = df[col].map({'Yes': 1, 'No': 0}).fillna(-1).astype(int)

    # Handle BMI outliers by clipping instead of filtering
    df['BMI'] = df['BMI'].clip(lower=10, upper=60)
    df.reset_index(drop=True, inplace=True)

    # === New Features ===
    # 1. Recovery duration in days
    df["Recovery_Duration"] = (df["Date_of_Recovery"] - df["Date_of_Infection"]).dt.days.fillna(0)
    # Avoid negative recovery durations
    df["Recovery_Duration"] = df["Recovery_Duration"].apply(lambda x: x if x >= 0 else 0)
    
    # 2. Time to reinfection (post recovery)
    df["Time_to_Reinfection"] = (df["Date_of_Reinfection"] - df["Date_of_Recovery"]).dt.days.fillna(0)
    df["Reinfected_Later"] = df["Time_to_Reinfection"].apply(lambda x: 1 if x > 0 else 0)

    # 3. Time between vaccination and infection
    df["Vaccine_to_Infection_Days"] = (df["Date_of_Infection"] - df["Date_of_Last_Dose"]).dt.days.fillna(0)

    # 4. Hospital stay duration
    df["Hospital_Stay_Duration"] = (df["Hospital_Discharge_Date"] - df["Hospital_Admission_Date"]).dt.days.fillna(0)
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
            known_classes = set(encoders[column].classes_)
            df[column] = df[column].apply(
                lambda x: encoders[column].transform([x])[0] if x in known_classes else 0
    )
        else:
            df[column] = pd.factorize(df[column])[0]
            
    # Fill any remaining NaNs to avoid issues during scaling
    df.fillna(0, inplace=True)
    
    # === Scaling the features ===
    scaled_data = scaler.transform(df)

    return scaled_data