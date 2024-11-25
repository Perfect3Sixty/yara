from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from services.search_api import SourceExtractorService
from typing import AsyncIterator, Dict, Any, List
import asyncio
import json, uuid
from datetime import datetime

class OpenAiService:
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        self.source_extractor = SourceExtractorService()

    async def get_embeddings(self, text: str) -> List[float]:
        """Get embeddings for text"""
        return await asyncio.to_thread(
            self.embeddings.embed_query,
            text
        )

    def format_sse(self, event: str, data: Any) -> str:
        """Format the data as SSE message with event type"""
        json_data = {
            "message_id": f'message-{uuid.uuid4()}',
            "type": "message",
            "content": data,
        }
        
        if event == "start" or event == "done" or event == "error":
            edge_json = {
                "event": event.upper(),
                "content": data,
            }
            return f"data: {edge_json}\n\n"
        
        return f"data: {json_data}\n\n"

    async def accumulate_chunks(self, current_chunk: List[str], buffer_size: int = 150) -> str:
        """Accumulate chunks until they form a meaningful segment"""
        text = ''.join(current_chunk).strip()
        if not text:
            return None
            
        if (text[-1] in '.!?' or len(text) >= buffer_size):
            return text
        return None

    async def get_last_user_message(self, messages: List[Any]) -> str:
        """Extract the last user message from various message formats"""
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                return msg.content
            elif isinstance(msg, dict) and msg.get("role") == "user":
                return msg["content"]
            elif hasattr(msg, "type") and msg.type == "human":
                return msg.content
        return ""

    async def enhance_messages_with_context(
        self,
        messages: List[Any]
    ) -> List[Any]:
        """Add source context to the conversation messages"""
        try:
            # Get the latest user message
            user_message = await self.get_last_user_message(messages)
            
            # Get context from sources
            sources = await self.source_extractor.get_source_context(user_message)
            context = self.source_extractor.format_context_for_prompt(sources)
            
            # Create new system message with context
            system_content = (
                "You are a beauty and skincare consultant. Use the following source "
                "information to provide accurate and informed responses. If the sources "
                "don't contain relevant information, use your general knowledge:\n\n"
                f"{context}\n\n"
            )
            
            # Filter out existing system messages and keep other messages
            enhanced_messages = []
            for msg in messages:
                if not (isinstance(msg, SystemMessage) or 
                       (isinstance(msg, dict) and msg.get("role") == "system")):
                    if isinstance(msg, (HumanMessage, AIMessage)):
                        enhanced_messages.append(msg)
                    elif isinstance(msg, dict):
                        if msg["role"] == "user":
                            enhanced_messages.append(HumanMessage(content=msg["content"]))
                        elif msg["role"] == "assistant":
                            enhanced_messages.append(AIMessage(content=msg["content"]))
            
            # Add new system message at the beginning
            return [SystemMessage(content=system_content)] + enhanced_messages
            
        except Exception as e:
            print(f"Error enhancing messages with context: {str(e)}")
            return messages

    async def chat_stream(
        self, 
        messages: List[Any], 
        temperature: float = 0.7
    ) -> AsyncIterator[str]:
        """Stream chat completions with proper SSE format"""
        try:
            # First enhance messages with context
            enhanced_messages = await self.enhance_messages_with_context(messages)
            
            callback_handler = AsyncIteratorCallbackHandler()
            llm = ChatOpenAI(
                streaming=True,
                callbacks=[callback_handler],
                temperature=temperature,
                model=self.model_name,
                openai_api_key=self.api_key,
                max_tokens=1000
            )

            current_chunk = []
            full_response = []
            
            # Send start message
            yield self.format_sse("start", "Gathering information...")
            
            async for chunk in llm.astream(enhanced_messages):
                if hasattr(chunk, 'content'):
                    token = chunk.content
                    current_chunk.append(token)
                    full_response.append(token)
                    
                    accumulated_text = await self.accumulate_chunks(current_chunk)
                    if accumulated_text:
                        yield self.format_sse("chunk", accumulated_text)
                        current_chunk = []

            # Send any remaining text
            remaining_text = ''.join(current_chunk).strip()
            if remaining_text:
                yield self.format_sse("chunk", remaining_text)

            # Send complete response
            complete_response = ''.join(full_response)
            yield self.format_sse("final", complete_response)
            yield self.format_sse("done", "Response completed")

        except Exception as e:
            yield self.format_sse("error", str(e))
        finally:
            if 'callback_handler' in locals():
                callback_handler.done.set()

    async def chat_completion(
        self, 
        messages: List[Any], 
        temperature: float = 0.7
    ) -> str:
        """Get single chat completion response"""
        try:
            # First enhance messages with context
            enhanced_messages = await self.enhance_messages_with_context(messages)
            
            llm = ChatOpenAI(
                streaming=False,
                temperature=temperature,
                model=self.model_name,
                openai_api_key=self.api_key
            )
            response = await llm.ainvoke(enhanced_messages)
            return response.content
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")