// src/app/page.js
"use client";

import { useState } from 'react';
import Layout from '../components/Layout';
import PatientForm from '../components/PatientForm';
import PredictionResults from '../components/PredictionResults';
import { predictReinfection } from '../utils/api';

export default function Home() {
  const [formData, setFormData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  
  const handleSubmit = async (patientData) => {
    setLoading(true);
    setError(null);
    setFormData(patientData);
    
    try {
      const response = await predictReinfection(patientData);
      setResult(response);
    } catch (error) {
      console.error('Prediction error:', error);
      setError('Failed to get prediction. Please check your connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full mb-6 shadow-lg">
            <span className="text-3xl">🦠</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            COVID-19 Reinfection Predictor
          </h1>
          <div className="max-w-3xl mx-auto">
            <p className="text-xl text-gray-600 mb-6 leading-relaxed">
              This application predicts the likelihood of COVID-19 reinfection based on patient data 
              using advanced machine learning and medical literature analysis.
            </p>
            <div className="flex flex-wrap justify-center gap-4 text-sm">
              <div className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full font-medium">
                🤖 AI-Powered Analysis
              </div>
              <div className="bg-green-100 text-green-800 px-4 py-2 rounded-full font-medium">
                📚 Evidence-Based
              </div>
              <div className="bg-purple-100 text-purple-800 px-4 py-2 rounded-full font-medium">
                🔬 Medical Literature RAG
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="max-w-7xl mx-auto">
          {/* Patient Form */}
          <PatientForm 
            onSubmit={handleSubmit} 
            isLoading={loading}
          />

          {/* Loading State */}
          {loading && (
            <div className="mt-8 text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-full mb-4 animate-spin">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Processing Prediction...</h3>
              <p className="text-gray-600">Analyzing patient data and consulting medical literature</p>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="mt-8 max-w-2xl mx-auto">
              <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <span className="text-2xl">⚠️</span>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-lg font-medium text-red-800">Prediction Error</h3>
                    <p className="text-red-700 mt-1">{error}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Results */}
          {result && !loading && (
            <PredictionResults 
              result={result} 
              patientData={formData}
            />
          )}
        </div>

        {/* Footer */}
        <div className="mt-5 text-center">
          <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="text-left">
                <h4 className="text-lg font-semibold text-gray-800 mb-2">🧬 How It Works</h4>
                <p className="text-gray-600 text-sm">
                  Our system combines a Random Forest machine learning model trained on COVID-19 
                  patient data with a Retrieval-Augmented Generation (RAG) system that analyzes 
                  scientific literature from PubMed to provide evidence-based risk assessments.
                </p>
              </div>
              {/* <div className="text-left">
                <h4 className="text-lg font-semibold text-gray-800 mb-2">⚕️ Medical Disclaimer</h4>
                <p className="text-gray-600 text-sm">
                  This tool is for informational purposes only and should not replace professional 
                  medical advice. Always consult with healthcare professionals for medical decisions 
                  and treatment recommendations.
                </p>
              </div> */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}