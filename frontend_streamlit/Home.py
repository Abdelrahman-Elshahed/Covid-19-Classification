import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(
    page_title="COVID-19 Reinfection Predictor",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API endpoint
API_URL = "http://127.0.0.1:8000/predict"

# Function to make prediction
def predict_reinfection(patient_data):
    try:
        response = requests.post(API_URL, json=[patient_data])
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None

# App title and description
st.title("COVID-19 Reinfection Predictor")
st.markdown("""
This application predicts the likelihood of COVID-19 reinfection based on patient data.
Fill in the form below with the patient details to get a prediction.
""")

# Create a form for user input
with st.form("patient_form"):
    st.subheader("Patient Information")
    
    # Create two columns for the form
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=0, max_value=120, value=70)
        gender = st.selectbox("Gender", ["Male", "Female"])
        region_options = ["Hovedstaden", "Sjælland", "Syddanmark", "Midtjylland", "Nordjylland"]
        region = st.selectbox("Region", region_options)
        preexisting_conditions = st.selectbox(
            "Preexisting Condition", 
            ["Diabetes","Asthma", "Hypertension", "Obesity", "Cardiovascular"]
        )
        covid_strain = st.selectbox(
            "COVID Strain", 
            ["Omicron", "Beta", "Delta", "Alpha", "XBB.1.5"]
        )
        symptoms = st.selectbox("Symptoms", [ "Moderate","Mild", "Severe"])
        severity = st.selectbox("Severity", [ "Moderate", "Low","High", "Critical"])
        hospitalized = st.selectbox("Hospitalized", ["Yes", "No"])
        
        if hospitalized == "Yes":
            hospital_admission_date = st.date_input(
                "Hospital Admission Date", 
                value=datetime(2023, 4, 18)
            )
            hospital_discharge_date = st.date_input(
                "Hospital Discharge Date", 
                value=datetime(2023, 4, 25)
            )
        else:
            hospital_admission_date = datetime.now() - timedelta(days=14)
            hospital_discharge_date = datetime.now() - timedelta(days=7)
        
    with col2:
        icu_admission = st.selectbox("ICU Admission", [ "No","Yes"])
        ventilator_support = st.selectbox("Ventilator Support", [ "No","Yes"])
        recovered = st.selectbox("Recovered", ["Yes", "No"])
        
        date_of_infection = st.date_input(
            "Date of Infection", 
            value=datetime(2023, 4, 15)
        )
        
        if recovered == "Yes":
            date_of_recovery = st.date_input(
                "Date of Recovery", 
                value=datetime(2023, 5, 10)
            )
        else:
            date_of_recovery = datetime.now()
            
        date_of_reinfection = st.date_input(
            "Date of Reinfection (if applicable, otherwise leave default)",
            value=datetime(2024, 5, 10)
        )
        
        vaccination_status = st.selectbox("Vaccination Status", ["Yes", "No"])
        
        if vaccination_status == "Yes":
            vaccine_type = st.selectbox(
                "Vaccine Type", 
                ["Pfizer", "Moderna", "AstraZeneca", "Janssen"]
            )
            doses_received = st.number_input("Doses Received", min_value=0, max_value=5, value=2)
            date_of_last_dose = st.date_input(
                "Date of Last Dose", 
                value=datetime(2023, 1, 15)
            )
        else:
            vaccine_type = "None"
            doses_received = 0
            date_of_last_dose = datetime.now() - timedelta(days=180)
    
    # Additional information
    st.subheader("Additional Information")
    col3, col4 = st.columns(2)
    
    with col3:
        long_covid_symptoms = st.selectbox(
            "Long COVID Symptoms", 
            [ "Fatigue", "Brain Fog", "Shortness of Breath","None", "Chest Pain"]
        )
        occupation = st.selectbox(
            "Occupation", 
            [ "Teacher","Healthcare", "Office Worker", "Driver", "Student", "Unemployed"]
        )
    
    with col4:
        smoking_status = st.selectbox("Smoking Status", ["Current", "Never", "Former"])
        bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=35.0, step=0.1)
        recovery_classification = st.selectbox(
            "Recovery Classification", 
            [ "Typical Recovery","Fast Recovery", "Delayed Recovery"]
        )
    
    # Submit button
    submit_button = st.form_submit_button("Predict Reinfection Risk")

# When form is submitted
if submit_button:
    # Construct patient data dictionary
    patient_data = {
        "Age": age,
        "Gender": gender,
        "Region": region,
        "Preexisting_Condition": preexisting_conditions,
        "Date_of_Infection": date_of_infection.strftime("%Y-%m-%dT00:00:00.000Z"),
        "COVID_Strain": covid_strain,
        "Symptoms": symptoms,
        "Severity": severity,
        "Hospitalized": hospitalized,
        "Hospital_Admission_Date": hospital_admission_date.strftime("%Y-%m-%dT00:00:00.000Z"),
        "Hospital_Discharge_Date": hospital_discharge_date.strftime("%Y-%m-%dT00:00:00.000Z"),
        "ICU_Admission": icu_admission,
        "Ventilator_Support": ventilator_support,
        "Recovered": recovered,
        "Date_of_Recovery": date_of_recovery.strftime("%Y-%m-%dT00:00:00.000Z"),
        "Date_of_Reinfection": date_of_reinfection.strftime("%Y-%m-%dT00:00:00.000Z"),
        "Vaccination_Status": vaccination_status,
        "Vaccine_Type": vaccine_type,
        "Doses_Received": doses_received,
        "Date_of_Last_Dose": date_of_last_dose.strftime("%Y-%m-%dT00:00:00.000Z"),
        "Long_COVID_Symptoms": long_covid_symptoms,
        "Occupation": occupation,
        "Smoking_Status": smoking_status,
        "BMI": bmi,
        "Recovery_Classification": recovery_classification
    }
    
    # Show prediction processing message
    with st.spinner("Processing prediction..."):
        # Call API for prediction
        result = predict_reinfection(patient_data)
    
    # Display prediction results
    if result:
        st.subheader("Prediction Results")
        
        # Create columns for results
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            # Display reinfection prediction with appropriate styling
            st.markdown("### Reinfection Risk:")
            if result["reinfection_prediction"] == "Yes":
                st.markdown(
                    f'<div style="background-color:#FFCCCB; padding:20px; border-radius:10px;">'
                    f'<h1 style="color:#B22222; text-align:center;">POSITIVE</h1>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div style="background-color:#CCFFCC; padding:20px; border-radius:10px;">'
                    f'<h1 style="color:#006400; text-align:center;">NEGATIVE</h1>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            # Show key risk factors
            st.markdown("### Key Risk Factors:")
            risk_factors = []
            
            if age > 65:
                risk_factors.append("- Advanced age (65+)")
            
            if preexisting_conditions != "None":
                risk_factors.append(f"- Preexisting condition: {preexisting_conditions}")
                
            if vaccination_status == "No":
                risk_factors.append("- Not vaccinated")
            elif doses_received < 2:
                risk_factors.append("- Inadequate vaccination (< 2 doses)")
                
            if severity in ["High", "Critical"]:
                risk_factors.append(f"- {severity} severity of initial infection")
                
            if bmi > 30:
                risk_factors.append("- Obesity (BMI > 30)")
                
            if smoking_status == "Current":
                risk_factors.append("- Current smoker")
                
            if not risk_factors:
                risk_factors.append("- No significant risk factors identified")
                
            for factor in risk_factors:
                st.markdown(factor)
                
        with res_col2:
            # Display the RAG analysis
            st.markdown("### Medical Literature Analysis:")
            
            # Extract and display risk level from description
            description = result["description"]
            
            # Format the description with proper markdown
            if "Based on the research, the risk level is" in description:
                risk_part = description.split("Based on the research, the risk level is")[1].split("\n")[0].strip()
                explanation_part = description.split("According to the evidence,")[1].strip()
            
                st.markdown(f"**Risk Level:** {risk_part}")
                st.markdown(f"**Evidence-Based Analysis:** {explanation_part}")
            else:
                st.markdown(description)

            
        # Optionally, you can add a section for recommendation
        st.subheader("Recommendations")
        
        # Basic recommendations based on vaccination status and other factors
        recommendations = []
        
        if vaccination_status == "No":
            recommendations.append("- Consider getting vaccinated to reduce reinfection risk")
        elif doses_received < 3:
            recommendations.append("- Consider getting additional vaccine doses as recommended")
            
        if bmi > 30:
            recommendations.append("- Managing weight can help reduce severity of COVID-19")
            
        if smoking_status == "Current":
            recommendations.append("- Quitting smoking can improve outcomes")
            
        recommendations.append("- Continue practicing preventive measures (masks, hand hygiene, etc.)")
        recommendations.append("- Monitor for symptoms and get tested if they develop")
        
        for rec in recommendations:
            st.markdown(rec)

# Add information about the app at the bottom
st.markdown("---")
st.markdown("### About This App")
st.markdown("""
This app uses a machine learning model trained on COVID-19 patient data to predict the risk of reinfection.
It also provides an analysis based on medical literature using a RAG (Retrieval-Augmented Generation) system.

The prediction considers various factors including demographics, medical history, vaccination status, and previous COVID-19 experience.
""")

# Add a section for system status
st.sidebar.title("System Status")
try:
    response = requests.get("http://127.0.0.1:8000/health")
    if response.status_code == 200:
        status_data = response.json()
        st.sidebar.success("✅ API Service: Online")
        st.sidebar.success("✅ Prediction Service: Available")
        st.sidebar.success("✅ RAG Analysis: Available") 
    else:
        st.sidebar.error("❌ API Service: Error")
except:
    st.sidebar.error("❌ API Service: Offline")

# Add reference information
st.sidebar.title("References")
st.sidebar.markdown("""
- COVID-19 Dataset: Classification data
- Model: Random Forest Classifier
- Medical Literature: PubMed abstracts
""")