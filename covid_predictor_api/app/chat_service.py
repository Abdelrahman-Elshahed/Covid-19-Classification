from typing import Dict, Any, Optional
import os
from datetime import datetime
import json

try:
    from RagModule.scripts.rag_pipeline import generate_explanation
    RAG_AVAILABLE = True
except Exception as e:
    print(f"Warning: RAG module not available for chat: {e}")
    RAG_AVAILABLE = False

class ChatService:
    def __init__(self):
        self.chat_history = {}
    
    def process_message(self, 
                        message: str, 
                        patient_context: Optional[Dict[str, Any]] = None,
                        session_id: str = "default") -> str:
        """
        Process a chat message from the user.
        
        Args:
            message: The user's message
            patient_context: Optional patient data for context
            session_id: Unique identifier for the chat session
            
        Returns:
            The assistant's response
        """
        # Initialize chat history for this session if it doesn't exist
        if session_id not in self.chat_history:
            self.chat_history[session_id] = []
        
        # Add the user message to history
        self.chat_history[session_id].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # If RAG is not available, provide a fallback response
        if not RAG_AVAILABLE:
            response = self._generate_fallback_response(message)
        else:
            # Use the RAG system to generate a response
            # If patient context is provided, use it for better answers
            if patient_context and "question" not in message:
                # Customize the question to include patient context
                query = f"Based on a patient with: Age {patient_context.get('Age', 'unknown')}, " \
                       f"Gender {patient_context.get('Gender', 'unknown')}, " \
                       f"COVID strain {patient_context.get('COVID_Strain', 'unknown')}, " \
                       f"and {patient_context.get('Preexisting_Condition', 'no')} preexisting condition, " \
                       f"{message}"
                       
                response = self._generate_rag_response(query)
            else:
                response = self._generate_rag_response(message)
        
        # Add the assistant's response to history
        self.chat_history[session_id].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def _generate_fallback_response(self, message: str) -> str:
        """Generate a fallback response when RAG is not available."""
        return (
            "I'm sorry, but the advanced medical knowledge system is currently unavailable. "
            "Please consult with a healthcare professional for specific medical advice about COVID-19. "
            "I can still try to provide general information, but cannot access the latest research or give personalized insights."
        )
    
    def _generate_rag_response(self, query: str) -> str:
        """Generate a response using the RAG system."""
        try:
            # Prepare a simulated patient object with minimal data
            # The actual query is passed as a custom field
            patient_obj = {
                "Age": 0,
                "Gender": "",
                "question": query
            }
            
            # Call the RAG generate_explanation function
            response = generate_explanation(patient_obj)
            
            # Clean up the response format if needed
            if response.startswith("[ RAG Medical Literature ]"):
                response = response.replace("[ RAG Medical Literature ]", "").strip()
                
            return response
        except Exception as e:
            print(f"Error generating RAG response: {e}")
            return (
                f"I encountered an error while retrieving information: {str(e)}. "
                "Please try rephrasing your question or ask something else."
            )

# Create a singleton instance
chat_service = ChatService()
