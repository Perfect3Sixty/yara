# processors/text_processor.py
from typing import AsyncIterator, List, Dict, Any, Optional
import uuid
from datetime import datetime
from services.openai import OpenAiService
from services.qdrant import get_qdrant_client
from schemas.chat import UserProfile, ChatMessage
from processors.agent.yara import YaraAgent
from core.config import OPENAI_API_KEY, OPENAI_MODEL

class TextProcessor:
    def __init__(self):
        self.openai = OpenAiService(OPENAI_API_KEY, OPENAI_MODEL)
        self.qdrant_client = get_qdrant_client()
        self.collection_name = "beauty_consultations"
        self.yara_agent = YaraAgent()

    async def get_session(self, session_id: str) -> Optional[Dict]:
        """Retrieve session data from Qdrant"""
        try:
            point = self.qdrant_client.retrieve(
                collection_name=self.collection_name,
                ids=[session_id]
            )
            return point[0] if point else None
        except Exception as e:
            print(f"Error retrieving session: {str(e)}")
            return None

    async def initialize_session(self, user_profile: UserProfile) -> str:
        """Initialize a new chat session with user profile"""
        try:
            session_id = str(uuid.uuid4())
            profile_text = self.yara_agent.get_profile_text(user_profile.dict())
            profile_embedding = await self.openai.get_embeddings(profile_text)
            
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[{
                    'id': session_id,
                    'vector': profile_embedding,
                    'payload': {
                        'profile': user_profile.dict(),
                        'messages': []
                    }
                }]
            )
            
            # Initialize memory for this session
            self.yara_agent.get_memory(session_id)
            return session_id
        except Exception as e:
            print(f"Error initializing session: {str(e)}")
            raise

    async def chat_stream(
        self,
        session_id: str,
        message: str
    ) -> AsyncIterator[str]:
        """Stream chat responses"""
        try:
            session_data = await self.get_session(session_id)
            if not session_data:
                yield '{"type": "error", "content": "Session not found"}'
                return

            messages = await self.yara_agent.prepare_messages(session_id, message, session_data)
            
            async for chunk in self.openai.chat_stream(messages):
                yield chunk

            # Get the AI's complete response from the last message
            ai_response = messages[-1].content if messages else ""
            
            # Update session with new messages
            await self._update_session(session_id, message, ai_response, session_data)
            
        except Exception as e:
            yield f'{{"type": "error", "content": "Error in chat stream: {str(e)}"}}'

    async def _update_session(
        self, 
        session_id: str, 
        user_message: str, 
        ai_response: str,
        session_data: Dict
    ):
        """Update session with new messages"""
        try:
            # Update agent's memory
            memory = self.yara_agent.get_memory(session_id)
            memory.add_user_message(user_message)
            memory.add_ai_message(ai_response)

            # Create new messages
            new_messages = [
                ChatMessage(
                    role="user",
                    content=user_message,
                    timestamp=datetime.now().isoformat()
                ).dict(),
                ChatMessage(
                    role="assistant",
                    content=ai_response,
                    timestamp=datetime.now().isoformat()
                ).dict()
            ]

            # Update payload
            updated_payload = {
                'profile': session_data.payload['profile'],
                'messages': session_data.payload['messages'] + new_messages
            }

            # Get new embedding
            profile_text = self.yara_agent.get_profile_text(session_data.payload['profile'])
            vector = await self.openai.get_embeddings(profile_text)
            
            # Update Qdrant
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[{
                    'id': session_id,
                    'vector': vector,
                    'payload': updated_payload
                }]
            )
        except Exception as e:
            print(f"Error updating session: {str(e)}")
            raise

    async def get_chat_history(self, session_id: str) -> List[ChatMessage]:
        """Retrieve chat history for a session"""
        try:
            session_data = await self.get_session(session_id)
            if not session_data:
                return []
            return [ChatMessage(**msg) for msg in session_data.payload['messages']]
        except Exception as e:
            print(f"Error retrieving chat history: {str(e)}")
            raise