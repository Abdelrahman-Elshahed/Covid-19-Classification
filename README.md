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
- Next.js
- Pandas & NumPy
- Scikit-learn
- Pydantic
- Uvicorn
- Joblib

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

```bash
Go to http://127.0.0.1:8000/docs to use the interactive Swagger UI.
```

## 📥 Example Request Body

```bash
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

---

## ✅ Expected Response Body

```bash
{
  "reinfection_prediction": "No",
  "description": "Non-Smoker, Normal BMI, No ICU history"
}
```

## Getting Started with the FrontEnd

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.js`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## 📁 Project Structure

```bash
covid_predictor/
├── covid_predictor_api/
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
├── data/
│ ├── splitted_data/
│ │   ├── X_test.csv         # Test set features
│ │   ├── X_train.csv        # Training set features
│ │   ├── y_test.csv         # Test set labels
│ │   └── y_train.csv        # Training set labels
│ ├── splitted_data_encoded/ 
│ │   ├── X_test.csv         # Test set features with encoding
│ │   ├── X_train.csv        # Training set features with encoding
│ │   ├── y_test.csv         # Test set labels with encoding
│ │   └── y_train.csv        # Training set labels with encoding
│ ├── covid1-19 Dataset.csv  # Data Used for training the model
│ └── Cleaned_Data.csv       # Cleaned and preprocessed dataset
│
├── frontend_next.js/
│ ├── app/
│ │   ├── page.js            # Main page component
│ │   ├── components/        # Reusable React components
│ │   └── styles/            # CSS/SCSS modules
│ ├── public/                # Static assets (images, icons, etc.)
│ ├── package.json           # Frontend dependencies and scripts
│ ├── next.config.js         # Next.js configuration
│ └── README.md              # Frontend-specific documentation
│
├── frontend_streamlit/
│   ├── pages/                  # Streamlit pages
│   │   └── COVID_Chatbot.py    # Streamlit chatbot interface
│   └── home.py                 # Main Streamlit application
│
├── notebooks/
│ ├── Data_Cleaning.ipynb       # Jupyter notebook for data cleaning
│ ├── Data_Splitting.ipynb      # Jupyter notebook for data splitting
│ ├── Encoding_Features.ipynb   # Jupyter notebook for encoding features
│ ├── EDA.ipynb                 # Exploratory Data Analysis notebook
│ ├── Model_Evaluation.ipynb    # Jupyter notebook for model evaluation
│ └── Model_Training.ipynb      # Jupyter notebook for model training
│
├── RagModule/
│ ├── data/                  # Data files for retrieval-augmented generation (RAG)
│ ├── scripts/               # Utility and pipeline scripts for RAG workflows
│ ├── tests/                 # Unit and integration tests for RAG components
│ ├── vector_store/          # Vector database files for document embeddings and retrieval
│ └── README.md              # Documentation for the RAG module
│
├── pyproject.toml           # Python project configuration 
│
├── requirements.txt
│ 
├── README.md                # Project documentation 
│
└── uv.lock                   # Uvicorn lock file for FastAPI server
```

---

## 🙌 Author
Mohamed Nasser
[LinkedIn](https://www.linkedin.com/in/mohamed-nasser-ahmed/) | [GitHub](https://github.com/Mohamed-NA)
