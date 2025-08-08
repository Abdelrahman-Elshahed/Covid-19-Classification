// src/components/PredictionResults.jsx
import { useState, useEffect } from 'react';

export default function PredictionResults({ result, patientData }) {
  const [riskFactors, setRiskFactors] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [riskLevel, setRiskLevel] = useState("");
  const [explanation, setExplanation] = useState("");

  // Determine risk factors based on patient data
  useEffect(() => {
    if (!patientData) return;
    
    const factors = [];
    
    if (patientData.Age > 65) {
      factors.push("Advanced age (65+)");
    }
    
    if (patientData.Preexisting_Condition && patientData.Preexisting_Condition !== "None") {
      factors.push(`Preexisting condition: ${patientData.Preexisting_Condition}`);
    }
    
    if (patientData.Vaccination_Status === "No") {
      factors.push("Not vaccinated");
    } else if (patientData.Doses_Received < 2) {
      factors.push("Inadequate vaccination (< 2 doses)");
    }
    
    if (patientData.Severity && ["High", "Critical"].includes(patientData.Severity)) {
      factors.push(`${patientData.Severity} severity of initial infection`);
    }
    
    if (patientData.BMI > 30) {
      factors.push("Obesity (BMI > 30)");
    }
    
    if (patientData.Smoking_Status === "Current") {
      factors.push("Current smoker");
    }
    
    if (factors.length === 0) {
      factors.push("No significant risk factors identified");
    }
    
    setRiskFactors(factors);
  }, [patientData]);

  // Determine recommendations based on patient data
  useEffect(() => {
    if (!patientData) return;
    
    const recs = [];
    
    if (patientData.Vaccination_Status === "No") {
      recs.push("Consider getting vaccinated to reduce reinfection risk");
    } else if (patientData.Doses_Received < 3) {
      recs.push("Consider getting additional vaccine doses as recommended");
    }
    
    if (patientData.BMI > 30) {
      recs.push("Managing weight can help reduce severity of COVID-19");
    }
    
    if (patientData.Smoking_Status === "Current") {
      recs.push("Quitting smoking can improve outcomes");
    }
    
    recs.push("Continue practicing preventive measures (masks, hand hygiene, etc.)");
    recs.push("Monitor for symptoms and get tested if they develop");
    
    setRecommendations(recs);
  }, [patientData]);

  // Parse the description from RAG analysis
  useEffect(() => {
    if (!result?.description) return;
    
    const description = result.description;
    
    if (description.includes("Based on the research, the risk level is")) {
      const riskPart = description.split("Based on the research, the risk level is")[1]?.split("\n")[0]?.trim();
      const explanationPart = description.split("According to the evidence,")[1]?.trim();
      
      setRiskLevel(riskPart || "");
      setExplanation(explanationPart || "");
    } else {
      setExplanation(description);
      setRiskLevel("");
    }
  }, [result]);

  if (!result) return null;

  const isPositive = result.reinfection_prediction === "Yes";

  return (
    <div className="mt-8 space-y-8">
      {/* Main Results Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">🦠 Prediction Results</h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column - Risk Status & Factors */}
        <div className="lg:col-span-1">
          <div className="space-y-6">
            {/* Reinfection Risk Status */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4 text-center">Reinfection Risk</h3>
              
              <div className={`rounded-lg p-6 text-center shadow-inner ${
                isPositive 
                  ? 'bg-gradient-to-br from-red-100 to-red-200 border-2 border-red-300' 
                  : 'bg-gradient-to-br from-green-100 to-green-200 border-2 border-green-300'
              }`}>
                <div className={`text-4xl font-bold mb-2 ${
                  isPositive ? 'text-red-700' : 'text-green-700'
                }`}>
                  {isPositive ? '⚠️ POSITIVE' : '✅ NEGATIVE'}
                </div>
                
                <div className={`text-sm font-medium ${
                  isPositive ? 'text-red-600' : 'text-green-600'
                }`}>
                  {isPositive ? 'Higher risk of reinfection' : 'Lower risk of reinfection'}
                </div>
              </div>
            </div>

            {/* Key Risk Factors */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                <span className="mr-2">🔍</span>
                Key Risk Factors
              </h3>
              
              <div className="space-y-3">
                {riskFactors.map((factor, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <div className="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                    <span className="text-gray-700">{factor}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right Column - Medical Literature Analysis */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-lg p-6 h-full">
            <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <span className="mr-2">📚</span>
              Medical Literature Analysis
            </h3>
            
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border-l-4 border-blue-500">
              {riskLevel && (
                <div className="mb-4">
                  <span className="text-sm font-medium text-gray-600">Risk Level Assessment:</span>
                  <div className="text-lg font-semibold text-blue-900 mt-1">
                    {riskLevel}
                  </div>
                </div>
              )}
              
              <div>
                <span className="text-sm font-medium text-gray-600">Evidence-Based Analysis:</span>
                <div className="text-gray-800 mt-2 leading-relaxed">
                  {explanation || result.description}
                </div>
              </div>
            </div>
            
            {/* ML Prediction Context */}
            {result.description.includes("ML Prediction:") && (
              <div className="mt-4 p-4 bg-purple-50 rounded-lg border-l-4 border-purple-400">
                <div className="text-sm text-purple-700">
                  <strong>AI Model Confidence:</strong> This prediction combines machine learning analysis 
                  with scientific literature to provide a comprehensive risk assessment.
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Recommendations Section */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-2xl font-semibold text-gray-800 mb-6 flex items-center">
          <span className="mr-2">💡</span>
          Recommendations
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recommendations.map((rec, index) => (
            <div key={index} className="flex items-start space-x-3 p-4 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg border-l-4 border-yellow-400">
              <div className="flex-shrink-0">
                <div className="w-6 h-6 bg-yellow-500 rounded-full flex items-center justify-center">
                  <span className="text-white text-xs font-bold">{index + 1}</span>
                </div>
              </div>
              <span className="text-gray-700">{rec}</span>
            </div>
          ))}
        </div>
      </div>

      {/* About Section */}
      <div className="border-t pt-6">
        <div className="bg-gradient-to-r from-gray-50 to-blue-50 rounded-lg p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-3 flex items-center">
            <span className="mr-2">ℹ️</span>
            About This Prediction
          </h3>
          
          <div className="text-gray-700 space-y-2">
            <p>
              This application uses a machine learning model trained on COVID-19 patient data to predict 
              the risk of reinfection. It also provides an analysis based on medical literature using a 
              RAG (Retrieval-Augmented Generation) system.
            </p>
            <p>
              The prediction considers various factors including demographics, medical history, vaccination 
              status, and previous COVID-19 experience.
            </p>
          </div>
          
          <div className="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
            <div className="bg-white rounded-lg p-3 shadow-sm">
              <div className="text-sm font-medium text-gray-600">Dataset</div>
              <div className="text-lg font-semibold text-blue-600">COVID-19 Classification</div>
            </div>
            <div className="bg-white rounded-lg p-3 shadow-sm">
              <div className="text-sm font-medium text-gray-600">Model</div>
              <div className="text-lg font-semibold text-green-600">Random Forest</div>
            </div>
            <div className="bg-white rounded-lg p-3 shadow-sm">
              <div className="text-sm font-medium text-gray-600">Literature</div>
              <div className="text-lg font-semibold text-purple-600">PubMed Abstracts</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}