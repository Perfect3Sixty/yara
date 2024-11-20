# schemas/chat.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid

class UserProfile(BaseModel):
    face_shape: Optional[str] = Field(description="User's face shape (e.g., oval, round, heart)")
    skin_type: Optional[str] = Field(description="User's skin type (e.g., oily, dry, combination)")
    skin_concerns: Optional[List[str]] = Field(description="List of skin concerns")
    hair_texture: Optional[str] = Field(description="Hair texture description")
    style_preferences: Optional[List[str]] = Field(description="Style preferences and aesthetics")
    budget_range: Optional[str] = Field(description="Preferred budget range for products")
    allergies: Optional[List[str]] = Field(description="List of known allergies")
    preferred_brands: Optional[List[str]] = Field(description="Preferred beauty brands")

class ChatMessage(BaseModel):
    role: str = Field(description="Role of the message sender (user/assistant)")
    content: str = Field(description="Content of the message")
    timestamp: Optional[str] = Field(description="Timestamp of the message")

class ChatSession(BaseModel):
    session_id: uuid.UUID
    user_profile: UserProfile
    messages: List[ChatMessage]
    
class ChatMessageRequest(BaseModel):
    message: str = Field(..., description="Message content from the user")
