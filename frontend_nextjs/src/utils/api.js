// src/utils/api.js
export const checkApiHealth = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/health');
    if (!response.ok) throw new Error('API response not ok');
    return await response.json();
  } catch (error) {
    console.error('Error checking API health:', error);
    return { status: 'offline' };
  }
};

export const predictReinfection = async (patientData) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify([patientData]),
    });
    
    if (!response.ok) throw new Error('Prediction failed');
    return await response.json();
  } catch (error) {
    console.error('Error predicting reinfection:', error);
    throw error;
  }
};

export const chatWithRag = async (question) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });
    
    if (!response.ok) throw new Error('Chat query failed');
    return await response.json();
  } catch (error) {
    console.error('Error querying RAG system:', error);
    throw error;
  }
};