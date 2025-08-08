// src/app/layout.js
import { Inter } from 'next/font/google';
import './globals.css';
import Link from 'next/link';
import SystemStatus from '../components/SystemStatus';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'COVID-19 Reinfection Predictor',
  description: 'Predict COVID-19 reinfection risk based on patient data',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex min-h-screen bg-gray-50">
          {/* Sidebar */}
          <div className="w-72 bg-gradient-to-b from-slate-800 to-slate-900 text-white shadow-xl">
            <div className="p-6">
              {/* Logo/Title */}
              <div className="flex items-center mb-8">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mr-3">
                  <span className="text-xl">🦠</span>
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white">COVID-19</h2>
                  <p className="text-sm text-slate-300">Prediction Suite</p>
                </div>
              </div>
              
              {/* Navigation */}
              <nav className="mb-8">
                <ul className="space-y-2">
                  <li>
                    <Link 
                      href="/" 
                      className="flex items-center px-4 py-3 rounded-lg hover:bg-slate-700 transition-colors duration-200 group"
                    >
                      <span className="mr-3 text-lg">🔬</span>
                      <div>
                        <div className="font-medium">Prediction Tool</div>
                        <div className="text-xs text-slate-400">ML-powered risk assessment</div>
                      </div>
                    </Link>
                  </li>
                  <li>
                    <Link 
                      href="/chatbot" 
                      className="flex items-center px-4 py-3 rounded-lg hover:bg-slate-700 transition-colors duration-200 group"
                    >
                      <span className="mr-3 text-lg">💬</span>
                      <div>
                        <div className="font-medium">Research Chatbot</div>
                        <div className="text-xs text-slate-400">RAG-powered Q&A system</div>
                      </div>
                    </Link>
                  </li>
                </ul>
              </nav>
              
              {/* System Status */}
              <div className="border-t border-slate-700 pt-6">
                <SystemStatus />
              </div>
              
              {/* References */}
              <div className="mt-6 border-t border-slate-700 pt-6">
                <h3 className="font-semibold mb-3 text-gray-200">📚 References</h3>
                <div className="space-y-2 text-sm text-slate-300">
                  <div className="flex items-start">
                    <span className="w-2 h-2 rounded-full bg-blue-400 mt-2 mr-2 flex-shrink-0"></span>
                    <span>COVID-19 Dataset: Classification data</span>
                  </div>
                  <div className="flex items-start">
                    <span className="w-2 h-2 rounded-full bg-green-400 mt-2 mr-2 flex-shrink-0"></span>
                    <span>Model: Random Forest Classifier</span>
                  </div>
                  <div className="flex items-start">
                    <span className="w-2 h-2 rounded-full bg-purple-400 mt-2 mr-2 flex-shrink-0"></span>
                    <span>Medical Literature: PubMed abstracts</span>
                  </div>
                </div>
              </div>
              
              {/* Version Info */}
              <div className="mt-8 pt-6 border-t border-slate-700 text-center">
                <p className="text-xs text-slate-400">Version 1.0.0</p>
                <p className="text-xs text-slate-400">© 2024 COVID-19 Research</p>
              </div>
            </div>
          </div>
          
          {/* Main content */}
          <main className="flex-1 overflow-auto">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}