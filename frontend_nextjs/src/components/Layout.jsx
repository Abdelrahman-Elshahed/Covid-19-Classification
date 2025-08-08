// src/components/Layout.jsx
import { useState, useEffect } from 'react';
import Link from 'next/link';
import Head from 'next/head';
import { checkApiHealth } from '../utils/api';

export default function Layout({ children, title = 'COVID-19 Prediction App' }) {
  const [apiStatus, setApiStatus] = useState({
    online: false,
    prediction: false,
    ragAnalysis: false
  });

  useEffect(() => {
    const checkStatus = async () => {
      const health = await checkApiHealth();
      setApiStatus({
        online: health.status === 'healthy',
        prediction: health.services?.includes('prediction'),
        ragAnalysis: health.services?.includes('RAG_explanation')
      });
    };
    
    checkStatus();
    // Check status every 30 seconds
    const interval = setInterval(checkStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content="COVID-19 Reinfection Prediction and Research Tool" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <div className="flex min-h-screen">
        {/* Sidebar */}
        <div className="w-64 bg-gray-100 p-4 flex flex-col">
          <h2 className="text-xl font-bold mb-4">COVID-19 Prediction</h2>
          
          <nav className="mb-8">
            <ul>
              <li className="mb-2">
                <Link href="/" className="hover:text-blue-600">
                  Prediction Tool
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/chatbot" className="hover:text-blue-600">
                  Research Chatbot
                </Link>
              </li>
            </ul>
          </nav>
          
          <div className="mt-auto">
            <h3 className="font-semibold mb-2">System Status</h3>
            <div className="text-sm">
              <div className={`flex items-center mb-1`}>
                <span className={`w-3 h-3 rounded-full mr-2 ${apiStatus.online ? 'bg-green-500' : 'bg-red-500'}`}></span>
                <span>API Service: {apiStatus.online ? 'Online' : 'Offline'}</span>
              </div>
              <div className={`flex items-center mb-1`}>
                <span className={`w-3 h-3 rounded-full mr-2 ${apiStatus.prediction ? 'bg-green-500' : 'bg-red-500'}`}></span>
                <span>Prediction Service: {apiStatus.prediction ? 'Available' : 'Unavailable'}</span>
              </div>
              <div className={`flex items-center`}>
                <span className={`w-3 h-3 rounded-full mr-2 ${apiStatus.ragAnalysis ? 'bg-green-500' : 'bg-red-500'}`}></span>
                <span>RAG Analysis: {apiStatus.ragAnalysis ? 'Available' : 'Unavailable'}</span>
              </div>
            </div>
            
            <div className="mt-4">
              <h3 className="font-semibold mb-2">References</h3>
              <ul className="text-sm list-disc pl-5">
                <li>COVID-19 Dataset: Classification data</li>
                <li>Model: Random Forest Classifier</li>
                <li>Medical Literature: PubMed abstracts</li>
              </ul>
            </div>
          </div>
        </div>
        
        {/* Main content */}
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </>
  );
}