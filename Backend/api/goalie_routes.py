"""Goalie AI chatbot routes - isolated feature."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class GoalieChatRequest(BaseModel):
    message: str
    pagePath: Optional[str] = "/"
    history: Optional[List[ChatMessage]] = []

class GoalieChatResponse(BaseModel):
    reply: str

@router.post("/chat")
async def chat_with_goalie(request: GoalieChatRequest) -> GoalieChatResponse:
    """Handle chat requests to Goalie AI assistant."""
    try:
        # Generate dynamic reply based on user message
        user_message = request.message.lower()
        original_message = request.message
        page_path = request.pagePath or "/"
        
        # Simple echo for testing - replace with LLM call when available
        reply = f"Goalie heard: '{original_message}' on page {page_path}. I'm here to help with Goalstone!"
        
        # Context-aware responses
        if any(word in user_message for word in ["hello", "hi", "hey"]):
            reply = f"Hello! I'm Goalie, your AI assistant. I see you're on {page_path}. How can I help you today?"
        elif any(word in user_message for word in ["help", "how", "what"]):
            reply = f"I can help you with Goalstone features! You're currently on {page_path}. What would you like to know?"
        elif any(word in user_message for word in ["goal", "goals"]):
            reply = "Goals are at the heart of Goalstone! I can help you create, track, and achieve your life goals with AI assistance."
        elif any(word in user_message for word in ["agent", "agents"]):
            reply = "Our AI agents specialize in career planning, financial advice, wellness coaching, and learning recommendations. Which area interests you?"
        elif any(word in user_message for word in ["thank", "thanks"]):
            reply = "You're welcome! I'm always here to help you make the most of Goalstone."
        else:
            # Dynamic response that includes the user's message
            reply = f"I understand you're asking about '{original_message}'. As your AI assistant, I'm here to help with Goalstone features and goal management. How can I assist you further?"
        
        return GoalieChatResponse(reply=reply)
        
    except Exception as e:
        # Log error locally without affecting other routes
        print(f"Goalie chat error: {str(e)}")
        return GoalieChatResponse(reply="I'm not available right now. Please try again later.")