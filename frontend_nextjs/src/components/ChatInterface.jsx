// src/components/ChatInterface.jsx
import { useState, useEffect, useRef } from 'react';
import { chatWithRag } from '../utils/api';

export default function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of chat when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: input }]);
    setInput('');
    setIsLoading(true);
    
    try {
      const response = await chatWithRag(input.trim());
      // Add assistant response
      setMessages(prev => [...prev, { role: 'assistant', content: response.response }]);
    } catch (error) {
      // Handle error
      setMessages(prev => [
        ...prev, 
        { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
  };

  const handleExampleClick = (question) => {
    setInput(question);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
                🔬 COVID-19 Research Chatbot
              </h1>
              <p className="text-gray-600">
                This chatbot uses a Retrieval-Augmented Generation (RAG) system to answer questions about COVID-19
                based on scientific literature from PubMed abstracts.
              </p>
            </div>
            {messages.length > 0 && (
              <button
                onClick={handleClearChat}
                className="bg-red-100 hover:bg-red-200 text-red-700 px-4 py-2 rounded-lg transition-colors"
              >
                🗑️ Clear Chat
              </button>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Main Chat Area */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow-lg h-[70vh] flex flex-col">
              {/* Chat Messages Area */}
              <div className="flex-1 overflow-y-auto p-6 bg-gray-50 rounded-t-lg">
                {messages.length === 0 ? (
                  <div className="text-center py-16">
                    <div className="text-6xl mb-4">🤖</div>
                    <h3 className="text-xl font-semibold text-gray-700 mb-2">Welcome to the COVID-19 Research Assistant</h3>
                    <p className="text-gray-500">Ask any question about COVID-19 to get started!</p>
                  </div>
                ) : (
                  <div className="space-y-6">
                    {messages.map((message, index) => (
                      <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[75%] ${
                          message.role === 'user' 
                            ? 'bg-blue-600 text-white' 
                            : 'bg-white border border-gray-200 text-gray-800'
                        } rounded-2xl p-4 shadow-sm`}>
                          <div className="flex items-start space-x-3">
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                              message.role === 'user' 
                                ? 'bg-blue-700 text-white' 
                                : 'bg-gray-200 text-gray-600'
                            }`}>
                              {message.role === 'user' ? '👤' : '🤖'}
                            </div>
                            <div className="flex-1">
                              <p className={`text-xs font-semibold mb-2 ${
                                message.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                              }`}>
                                {message.role === 'user' ? 'You' : 'Assistant'}
                              </p>
                              <div className="whitespace-pre-wrap leading-relaxed">
                                {message.content}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                    
                    {isLoading && (
                      <div className="flex justify-start">
                        <div className="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm max-w-[75%]">
                          <div className="flex items-start space-x-3">
                            <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-sm font-bold text-gray-600">
                              🤖
                            </div>
                            <div className="flex-1">
                              <p className="text-xs font-semibold mb-2 text-gray-500">Assistant</p>
                              <div className="flex items-center space-x-2">
                                <div className="flex space-x-1">
                                  <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce"></div>
                                  <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce" style={{animationDelay: '0.2s'}}></div>
                                  <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce" style={{animationDelay: '0.4s'}}></div>
                                </div>
                                <span className="text-sm text-gray-500">Searching medical literature...</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                    <div ref={messagesEndRef} />
                  </div>
                )}
              </div>
              
              {/* Input Area */}
              <div className="p-6 bg-white border-t border-gray-200 rounded-b-lg">
                <form onSubmit={handleSendMessage} className="flex space-x-4">
                  <div className="flex-1 relative">
                    <input
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      placeholder="Ask a question about COVID-19..."
                      className="w-full border border-gray-300 rounded-xl p-4 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      disabled={isLoading}
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={isLoading || !input.trim()}
                    className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-6 py-4 rounded-xl font-semibold transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:transform-none shadow-lg"
                  >
                    {isLoading ? (
                      <div className="w-6 h-6">
                        <svg className="animate-spin w-6 h-6" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                      </div>
                    ) : (
                      '📤 Send'
                    )}
                  </button>
                </form>
              </div>
            </div>
          </div>
          
          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            {/* About Section */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="font-bold text-lg text-gray-800 mb-4 flex items-center">
                ℹ️ About this Chatbot
              </h3>
              <div className="space-y-4 text-sm text-gray-600">
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">📚 Data Sources</h4>
                  <p>PubMed abstracts related to COVID-19</p>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">🔧 Technologies</h4>
                  <ul className="space-y-1">
                    <li>• Langchain</li>
                    <li>• FAISS vector database</li>
                    <li>• Azure OpenAI</li>
                  </ul>
                </div>
              </div>
            </div>
            
            {/* Example Questions */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="font-bold text-lg text-gray-800 mb-4 flex items-center">
                💡 Example Questions
              </h3>
              <div className="space-y-3">
                {[
                  "How effective are vaccines against new variants?",
                  "How does vaccination impact reinfection rates?",
                  "What is the likelihood of reinfection after recovery?",
                  "How does age affect COVID-19 outcomes?",
                  "What are the common symptoms of Long COVID?"
                ].map((question, i) => (
                  <button
                    key={i}
                    onClick={() => handleExampleClick(question)}
                    disabled={isLoading}
                    className="w-full text-left text-sm bg-gray-50 hover:bg-blue-50 border border-gray-200 hover:border-blue-300 p-3 rounded-lg transition-all duration-200 disabled:opacity-50"
                  >
                    <span className="text-blue-600 font-medium">Q:</span> {question}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}