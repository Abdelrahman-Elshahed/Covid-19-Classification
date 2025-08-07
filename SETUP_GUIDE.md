# COVID-19 Reinfection Prediction System

## System Architecture

This system consists of three main components:

1. **FastAPI Backend** (`covid_predictor_api/`) - Handles predictions and RAG-powered explanations
2. **Vite React Frontend** (`frontend_vite/`) - User interface with chat functionality
3. **RAG Module** (`RagModule/`) - Medical knowledge retrieval and AI chat

## Setup Instructions

### 1. Backend Setup (FastAPI)

```bash
# Navigate to the backend directory
cd covid_predictor_api

# Install dependencies (if not already done)
pip install fastapi uvicorn pydantic pandas numpy scikit-learn joblib python-dotenv

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

### 2. Frontend Setup (Vite React)

```bash
# Navigate to the frontend directory
cd frontend_vite

# Install dependencies (if not already done)
pnpm install

# Start the development server
pnpm dev
```

The frontend will be available at: http://localhost:5173

### 3. RAG Module Setup (Optional - for AI Chat)

```bash
# Set up Azure OpenAI credentials in .env file in the root directory
AZURE_API_KEY=your_azure_openai_api_key
AZURE_API_VERSION=2023-12-01-preview
AZURE_ENDPOINT=https://your-resource.openai.azure.com/
DEPLOYMENT_NAME=your-deployment-name
```

If you don't have Azure OpenAI access, the system will work with fallback responses.

## Features

### 1. Patient Data Input
- Comprehensive form with all COVID-19 related fields
- Input validation and data type conversion
- Date handling for temporal data

### 2. Prediction Service
- **Endpoint**: `POST /predict`
- Uses trained ML model for reinfection prediction
- Returns prediction with RAG-powered medical explanation

### 3. Chat Interface
- **Endpoint**: `POST /chat`
- RAG-powered medical assistant
- Context-aware responses using patient data
- Medical literature retrieval

### 4. Health Monitoring
- **Endpoint**: `GET /health`
- Service status monitoring
- RAG availability check

## API Endpoints

### Prediction
```http
POST http://localhost:8000/predict
Content-Type: application/json

[{
    "Age": 45,
    "Gender": "Male",
    "Region": "Hovedstaden",
    "Preexisting_Condition": "Diabetes",
    "Date_of_Infection": "2024-01-15T00:00:00Z",
    "COVID_Strain": "Omicron",
    "Symptoms": "Moderate",
    "Severity": "Moderate",
    "Hospitalized": "No",
    "Hospital_Admission_Date": "2024-01-15T00:00:00Z",
    "Hospital_Discharge_Date": "2024-01-20T00:00:00Z",
    "ICU_Admission": "No",
    "Ventilator_Support": "No",
    "Recovered": "Yes",
    "Date_of_Recovery": "2024-01-25T00:00:00Z",
    "Date_of_Reinfection": "2024-03-15T00:00:00Z",
    "Vaccination_Status": "Yes",
    "Vaccine_Type": "Pfizer",
    "Doses_Received": 3,
    "Date_of_Last_Dose": "2023-10-01T00:00:00Z",
    "Long_COVID_Symptoms": "Fatigue",
    "Occupation": "Teacher",
    "Smoking_Status": "Never",
    "BMI": 27.5,
    "Recovery_Classification": "Typical Recovery"
}]
```

### Chat
```http
POST http://localhost:8000/chat
Content-Type: application/json

{
    "message": "What factors affect COVID-19 reinfection risk?",
    "patient_context": {
        "Age": 45,
        "Gender": "Male",
        "COVID_Strain": "Omicron",
        "Preexisting_Condition": "Diabetes"
    },
    "session_id": "user123"
}
```

## User Flow

1. **User fills out patient form** with comprehensive COVID-19 data
2. **Form submits to FastAPI** `/predict` endpoint
3. **Backend processes data**:
   - Preprocesses and validates input
   - Runs ML model prediction
   - Generates RAG explanation
4. **Results displayed** with prediction and medical analysis
5. **User can interact with chatbot** for additional questions
6. **Chat uses RAG system** for medical knowledge retrieval

## Data Processing Pipeline

1. **Input Validation**: Pydantic models ensure data integrity
2. **Preprocessing**: 
   - Date normalization and timezone handling
   - Categorical encoding using pre-trained encoders
   - Feature scaling with saved scaler
   - New feature engineering (recovery duration, etc.)
3. **Prediction**: Trained ML model (Random Forest)
4. **Explanation**: RAG system retrieves relevant medical literature

## Configuration

### FastAPI Settings
- **Host**: `0.0.0.0`
- **Port**: `8000`
- **CORS**: Enabled for frontend domains

### Frontend Settings
- **API Base URL**: `http://localhost:8000`
- **Dev Port**: `5173`

### RAG Settings
- **Vector Store**: FAISS with HuggingFace embeddings
- **LLM**: Azure OpenAI GPT-4
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`

## Troubleshooting

### Backend Issues
- Ensure model files exist in `covid_predictor_api/model/`
- Check Python dependencies are installed
- Verify port 8000 is available

### Frontend Issues
- Check Node.js and pnpm are installed
- Verify API connection in browser dev tools
- Ensure all UI components are properly imported

### RAG Issues
- Verify Azure OpenAI credentials in `.env`
- Check vector store exists in `RagModule/vectorstore/`
- Review medical literature data in `RagModule/data/`

## File Structure
```
Covid-19-Classification/
├── covid_predictor_api/          # FastAPI Backend
│   ├── main.py                   # Main API application
│   ├── app/
│   │   ├── schemas.py           # Pydantic models
│   │   ├── model_interface.py   # ML model interface
│   │   ├── preprocessing.py     # Data preprocessing
│   │   └── chat_service.py      # Chat functionality
│   └── model/                   # Trained ML models
├── frontend_vite/               # React Frontend
│   ├── src/
│   │   ├── components/          # UI components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API client
│   │   └── App.jsx             # Main app
│   └── package.json
├── RagModule/                   # RAG System
│   ├── scripts/
│   │   ├── rag_pipeline.py     # Main RAG logic
│   │   ├── build_vectorstore.py
│   │   └── fetch_pubmed.py
│   ├── data/                   # Medical literature
│   └── vectorstore/           # Vector embeddings
└── data/                      # Training data
```

This system provides a complete end-to-end solution for COVID-19 reinfection prediction with AI-powered medical explanations.
