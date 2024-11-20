# processors/agent/yara.py
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from typing import Dict, Any, List
import json

class YaraAgent:
    def __init__(self):
        self.message_histories: Dict[str, ChatMessageHistory] = {}

    def get_memory(self, session_id: str) -> ChatMessageHistory:
        """Get or create message history for a session"""
        if session_id not in self.message_histories:
            self.message_histories[session_id] = ChatMessageHistory()
        return self.message_histories[session_id]

    def get_profile_text(self, profile: Dict[str, Any]) -> str:
        """Format profile text for embedding"""
        return f"""Face Shape: {profile.get('face_shape', 'Not specified')}
        Skin Type: {profile.get('skin_type', 'Not specified')}
        Skin Concerns: {', '.join(profile.get('skin_concerns', []) or ['Not specified'])}
        Hair Texture: {profile.get('hair_texture', 'Not specified')}
        Style Preferences: {', '.join(profile.get('style_preferences', []) or ['Not specified'])}
        Budget Range: {profile.get('budget_range', 'Not specified')}"""

    def _get_system_prompt(self, context: Dict[str, Any]) -> str:
        """Create system prompt with context"""
        return f"""You are Yara, an AI beauty consultant who provides personalized beauty advice.
        Current User Profile:
        - Face Shape: {context.get('face_shape', 'Not specified')}
        - Skin Type: {context.get('skin_type', 'Not specified')}
        - Skin Concerns: {', '.join(context.get('skin_concerns', []) or ['Not specified'])}
        - Hair Texture: {context.get('hair_texture', 'Not specified')}
        - Style Preferences: {', '.join(context.get('style_preferences', []) or ['Not specified'])}
        - Budget Range: {context.get('budget_range', 'Not specified')}
        - Allergies: {', '.join(context.get('allergies', []) or ['None specified'])}
        - Preferred Brands: {', '.join(context.get('preferred_brands', []) or ['Not specified'])}

        Based on this profile, provide personalized beauty advice and product recommendations.
        Always consider their specific features, preferences, and constraints when making suggestions.
        If recommending products, consider their budget range and any allergies.
        
        When recommending products:
        1. Always mention why the product is particularly good for their skin type and concerns
        2. Consider their budget range and allergies
        3. If suggesting high-end products, also provide more affordable alternatives
        4. Note any ingredients that specifically target their skin concerns
        5. Where relevant, mention how the product fits with their style preferences
        
        Keep responses friendly, professional, and well-structured."""

    async def prepare_messages(
        self, 
        session_id: str, 
        message: str, 
        session_data: Dict
    ) -> List[Dict]:
        """Prepare messages for chat completion"""
        context = session_data.payload['profile']
        message_history = self.get_memory(session_id)
        
        # Load history if not already loaded
        if not message_history.messages:
            for msg in session_data.payload['messages']:
                if msg['role'] == 'user':
                    message_history.add_user_message(msg['content'])
                else:
                    message_history.add_ai_message(msg['content'])

        # Prepare messages
        return [
            SystemMessage(content=self._get_system_prompt(context)),
            *message_history.messages,
            HumanMessage(content=message)
        ]