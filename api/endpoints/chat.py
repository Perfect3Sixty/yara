# api/endpoints/chat.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from schemas.chat import UserProfile, ChatMessage, ChatMessageRequest
from processors.text_processor import TextProcessor
from typing import Union, Dict, Any
router = APIRouter()
processor = TextProcessor()

@router.post("/chat/initialize")
async def initialize_chat(user_profile: UserProfile):
    """Initialize a new chat session with user profile"""
    try:
        session_id = await processor.initialize_session(user_profile)
        return {"session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/{session_id}/stream")
async def stream_chat(
    session_id: str, 
    chat_request: ChatMessageRequest
):
    """Stream chat responses"""
    return StreamingResponse(
        processor.chat_stream(session_id, chat_request.message),
        media_type="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'text/event-stream',
            'Access-Control-Allow-Origin': '*',
            'X-Accel-Buffering': 'no'
        }
    )
    


@router.get("/chat/{session_id}/history")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    try:
        history = await processor.get_chat_history(session_id)
        return {"history": [msg.dict() for msg in history]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))