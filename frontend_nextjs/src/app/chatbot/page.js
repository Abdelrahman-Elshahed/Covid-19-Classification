"use client";

import { useState, useRef, useEffect } from 'react';
import { chatWithRag } from '@/utils/api';

export default function ChatbotPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await chatWithRag(userMessage);
      setMessages(prev => [...prev, { role: 'assistant', content: response.response }]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'Sorry, I encountered an error connecting to the medical literature database. Please try again.' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-full mx-auto h-screen flex flex-col">
        <div className="bg-white shadow-lg overflow-hidden flex-1 flex flex-col">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 flex-shrink-0">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-4xl font-bold flex items-center">🔬 COVID-19 Research Chatbot</h1>
                <p className="mt-2 text-blue-100 text-base">
                  This chatbot uses a Retrieval-Augmented Generation (RAG) system to answer questions about COVID-19 
                  based on scientific literature from PubMed abstracts. Ask any question related to COVID-19, such as
                  transmission, symptoms, vaccination, reinfection risk, or treatments.
                </p>
              </div>
              <button
                onClick={clearChat}
                className="bg-white/20 hover:bg-white/30 transition-colors px-4 py-2 rounded-lg text-base font-medium"
              >
                Clear Chat
              </button>
            </div>
          </div>

          {/* Chat Container */}
          <div className="flex flex-1 min-h-0">
            {/* Chat Messages */}
            <div className="flex-1 flex flex-col">
              <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
                {messages.length === 0 ? (
                  <div className="text-center text-gray-500 py-12">
                    <div className="text-6xl mb-4">🧬</div>
                    <h3 className="text-2xl font-semibold mb-2">Welcome to the COVID-19 Research Chatbot</h3>
                    <p className="text-base text-gray-400 mb-6">Ask a question to start exploring medical literature</p>

                    <div className="bg-white rounded-lg p-4 max-w-md mx-auto text-left">
                      <h4 className="font-semibold text-gray-700 mb-3 text-base">Try asking:</h4>
                      <ul className="text-base space-y-2 text-gray-700">
                        {[
                          "How effective are vaccines against new variants?",
                          "How does vaccination impact reinfection rates?",
                          "What is the likelihood of reinfection after recovery?",
                          "How does age affect COVID-19 outcomes?",
                          "What are the common symptoms of Long COVID?"
                        ].map((question, index) => (
                          <li key={index} className="hover:text-blue-600 cursor-pointer" onClick={() => setInput(question)}>
                            • {question}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4 text-base leading-relaxed">
                    {messages.map((message, index) => (
                      <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] rounded-lg p-4 ${
                          message.role === 'user'
                            ? 'bg-blue-600 text-white'
                            : 'bg-white border shadow-sm'
                        }`}>
                          <div className="flex items-center mb-2">
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold mr-2 ${
                              message.role === 'user'
                                ? 'bg-blue-800 text-white'
                                : 'bg-gray-100 text-gray-700'
                            }`}>
                              {message.role === 'user' ? '👤' : '🤖'}
                            </div>
                            <span className={`text-sm font-medium ${
                              message.role === 'user' ? 'text-blue-100' : 'text-gray-700'
                            }`}>
                              {message.role === 'user' ? 'You' : 'Medical Assistant'}
                            </span>
                          </div>
                          <div className={`whitespace-pre-wrap text-base md:text-lg leading-relaxed ${
                            message.role === 'user' ? 'text-white' : 'text-gray-800'
                          }`}>{message.content}</div>
                        </div>
                      </div>
                    ))}

                    {isLoading && (
                      <div className="flex justify-start">
                        <div className="max-w-[80%] bg-white border shadow-sm rounded-lg p-4">
                          <div className="flex items-center mb-2">
                            <div className="w-8 h-8 rounded-full bg-gray-100 text-gray-700 flex items-center justify-center text-sm font-semibold mr-2">🤖</div>
                            <span className="text-sm font-medium text-gray-700">Medical Assistant</span>
                          </div>
                          <div className="flex items-center space-x-2 text-base">
                            <div className="text-gray-800">Searching medical literature...</div>
                            <div className="flex space-x-1">
                              <div className="w-2 h-2 rounded-full bg-blue-400 animate-bounce"></div>
                              <div className="w-2 h-2 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                              <div className="w-2 h-2 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                    <div ref={messagesEndRef} />
                  </div>
                )}
              </div>

              {/* Input Form */}
              <div className="p-4 bg-white border-t flex-shrink-0">
                <form onSubmit={handleSendMessage} className="flex space-x-2">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask a question about COVID-19..."
                    className="flex-1 text-base border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={isLoading}
                  />
                  <button
                    type="submit"
                    disabled={isLoading || !input.trim()}
                    className={`text-base px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                      isLoading || !input.trim()
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : 'bg-blue-600 hover:bg-blue-700 text-white shadow-md hover:shadow-lg transform hover:scale-105'
                    }`}
                  >
                    {isLoading ? (
                      <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    ) : (
                      'Send'
                    )}
                  </button>
                </form>
              </div>
            </div>

            {/* Sidebar */}
            <div className="w-72 bg-gray-100 p-4 border-l overflow-y-auto">
              <div className="space-y-4 text-sm">
                <div>
                  <h3 className="text-lg font-semibold text-gray-800 mb-2">📚 About this Chatbot</h3>
                  <div className="text-x text-gray-800 space-y-2">
                    <div className="bg-white p-2 rounded border-l-4 border-blue-400">
                      <h4 className="font-semibold text-blue-800 text-sm">Data Sources</h4>
                      <p>PubMed abstracts related to COVID-19</p>
                    </div>
                    <div className="bg-white p-2 rounded border-l-4 border-green-400">
                      <h4 className="font-semibold text-green-600 text-sm">Technologies</h4>
                      <ul className="mt-1 space-y-1">
                        <li>• Langchain</li>
                        <li>• FAISS vector database</li>
                        <li>• Azure OpenAI</li>
                      </ul>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-600 mb-2">💡 Example Questions</h3>
                  <div className="space-y-1">
                    {[
                      "How effective are vaccines against new variants?",
                      "How does vaccination impact reinfection rates?",
                      "What is the likelihood of reinfection after recovery?",
                      "How does age affect COVID-19 outcomes?",
                      "What are the common symptoms of Long COVID?"
                    ].map((question, index) => (
                      <button
                        key={index}
                        onClick={() => setInput(question)}
                        className="w-full text-left p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors duration-200 text-base"
                      >
                        • {question}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="bg-white p-3 rounded-lg border">
                  <h4 className="font-semibold text-gray-800 mb-2 text-base">ℹ️ How it works</h4>
                  <p className="text-sm text-gray-600">
                    This chatbot searches through thousands of medical research papers to provide evidence-based answers about COVID-19. All responses are grounded in scientific literature.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
