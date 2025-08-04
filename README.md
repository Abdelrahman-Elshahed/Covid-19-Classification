# COVID-19 Reinfection Prediction

A complete ML pipeline for predicting COVID-19 reinfection. Includes data cleaning, encoding, feature engineering, model training, evaluation, and deployment using FastAPI. The system accepts structured patient data and returns real-time predictions.

---

## 🚀 Project Overview

This project processes medical records to predict **Reinfection** cases using a trained classification model. It includes:
- Cleaned and preprocessed healthcare dataset.
- Feature engineering and standardization.
- A trained ML model for binary classification.
- FastAPI backend to expose the model for inference.
- React.js frontend for users to use the model.

---

## 🧠 Technologies Used

- Python
- FastAPI
- React.js
- Pandas & NumPy
- Scikit-learn
- Pydantic
- Uvicorn
- Joblib

---

## 📁 Project Structure
```
covid_predictor/
│
├── data/
│ └── covid1-19 Dataset.csv # Data Used for training the model
│
├── notebooks/
│ └── EDA.ipynb
│
├── covid_reinfection_api/
│ ├── main.py # FastAPI endpoint
│ ├── app/
│ │   ├── model_interface.py # Loads the trained model and scaler
│ │   ├── preprocessing.py   # Feature engineering and transformation logic
│ │   └── schemas.py         # Input schema using Pydantic
│ └── model/
│     ├── encoders.pkl       # Saved LabelEncoders for categorical features
│     ├── model.pkl          # Best Trained ML model (binary classifier)
│     └── scaler.pkl         # trained scaler used for scaling the input
│
├── utils/
│ └── encoder_mappings.pkl # Saved LabelEncoders for categorical features
│
├── requirements.txt # Project dependencies
└── README.md # Project documentation
```

---

## 🧪 How to Run the API

1. **Clone the repo:**

```bash
git clone https://github.com/your-username/covid_predictor
cd covid_predictor
```

2. **install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the API:**
```bash
uvicorn ./main:app --reload
```

4. **Test the API:**
```
Go to http://127.0.0.1:8000/docs to use the interactive Swagger UI.
```

## 📥 Example Request Body
```
[{
  "Age": 45,
  "Gender": "Male",
  "Region": "Hovedstaden",
  "Preexisting_Condition": "Diabetes",
  "Date_of_Infection": "2023-04-15",
  "COVID_Strain": "Omicron",
  "Symptoms": "Mild",
  "Severity": "Moderate",
  "Hospitalized": "Yes",
  "Hospital_Admission_Date": "2023-04-18",
  "Hospital_Discharge_Date": "2023-04-25",
  "ICU_Admission": "No",
  "Ventilator_Support": "No",
  "Recovered": "Yes",
  "Date_of_Recovery": "2023-05-10",
  "Reinfection": "No",
  "Date_of_Reinfection": "1900-01-01",  
  "Vaccination_Status": "Yes",
  "Vaccine_Type": "Pfizer",
  "Doses_Received": 2,
  "Date_of_Last_Dose": "2023-01-15",
  "Long_COVID_Symptoms": "Fatigue",  
  "Occupation": "Teacher",
  "Smoking_Status": "Former",
  "BMI": 25.3,
  "Recovery_Classification": "Fast Recovery"
}]
```

## ✅ Expected Response Body
```
{
  "reinfection_prediction": "No",
  "description": "Non-Smoker, Normal BMI, No ICU history"
}
```

---

## 🙌 Author
Mohamed Nasser
[LinkedIn](https://www.linkedin.com/in/mohamed-nasser-ahmed/) | [GitHub](https://github.com/Mohamed-NA)
