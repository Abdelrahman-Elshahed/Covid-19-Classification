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

## Rag Module


### 1️⃣ Overview

This module implements a *Retrieval-Augmented Generation (RAG)* pipeline to provide evidence-based explanations for *COVID-19 reinfection risk*.
It uses:

* *FAISS* for vector search over PubMed abstracts.
* *HuggingFace sentence-transformers* for embeddings.
* *Google Generative AI (Gemini)* for LLM responses.

---

### 2️⃣ Environment Setup

```bash
# Create virtual environment
python -m venv CovidRag
source CovidRag/bin/activate   # Linux/Mac
CovidRag\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

---

### 3️⃣ Environment Variables (.env)

```ini
GOOGLE_API_KEY=your_google_api_key
HUGGINGFACEHUB_API_TOKEN=your_hf_token
```

> Get HuggingFace token from: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

### 4️⃣ Usage

*Step 1 – Fetch PubMed abstracts*

```bash
python scripts/fetch_pubmed.py
```

*Step 2 – Build FAISS vector store*

```bash
python scripts/build_vectorstore.py
```

*Step 3 – Run RAG pipeline*

```bash
python scripts/rag_pipeline.py
```

---

### 5️⃣ Testing

```bash
# Test only retrieval
python test/test_retrieval.py

# Test full RAG flow
python test/test_rag_pipeline.py
```

---

### 6️⃣ Key Components

* *Embeddings Model*: sentence-transformers/all-MiniLM-L6-v2
* *LLM Model*: gemini-2.5-pro (Google Generative AI)
* *Retriever*: FAISS index over chunked PubMed abstracts
* *Prompt*: Medical assistant style, structured output

---

### 7️⃣ Prompt

![WhatsApp Image 2025-08-08 at 23 30 38](https://github.com/user-attachments/assets/4de6d1ee-8ffe-4f8c-b8f1-b663c460ef11)


## 🙌 Author
Mohamed Nasser
[LinkedIn](https://www.linkedin.com/in/mohamed-nasser-ahmed/) | [GitHub](https://github.com/Mohamed-NA)
