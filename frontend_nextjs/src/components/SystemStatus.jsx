// src/components/SystemStatus.jsx
"use client";

import { useEffect, useState } from 'react';

export default function SystemStatus() {
  const [apiStatus, setApiStatus] = useState({
    online: false,
    prediction: false,
    ragAnalysis: false
  });

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/health');
        if (response.ok) {
          const health = await response.json();
          setApiStatus({
            online: health.status === 'healthy',
            prediction: health.services?.includes('prediction'),
            ragAnalysis: health.services?.includes('RAG_explanation')
          });
        }
      } catch (error) {
        setApiStatus({
          online: false,
          prediction: false,
          ragAnalysis: false
        });
      }
    };
    
    checkStatus();
    const interval = setInterval(checkStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <h3 className="font-semibold mb-3 text-gray-200">📊 System Status</h3>
      <div className="space-y-2 text-sm">
        <div className="flex items-center">
          <span className={`w-3 h-3 rounded-full mr-2 ${apiStatus.online ? 'bg-green-500' : 'bg-red-500'}`}></span>
          <span className="text-slate-300">API Service: {apiStatus.online ? 'Online' : 'Offline'}</span>
        </div>
        <div className="flex items-center">
          <span className={`w-3 h-3 rounded-full mr-2 ${apiStatus.prediction ? 'bg-green-500' : 'bg-red-500'}`}></span>
          <span className="text-slate-300">Prediction Service: {apiStatus.prediction ? 'Available' : 'Unavailable'}</span>
        </div>
        <div className="flex items-center">
          <span className={`w-3 h-3 rounded-full mr-2 ${apiStatus.ragAnalysis ? 'bg-green-500' : 'bg-red-500'}`}></span>
          <span className="text-slate-300">RAG Analysis: {apiStatus.ragAnalysis ? 'Available' : 'Unavailable'}</span>
        </div>
      </div>
    </>
  );
}
