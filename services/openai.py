# services/openai.py
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import AsyncIterator, Dict, Any, List
import asyncio
import json, uuid
from datetime import datetime

class OpenAiService:
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)

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
            
        # If text ends with sentence-ending punctuation or is longer than buffer_size
        if (text[-1] in '.!?' or len(text) >= buffer_size):
            return text
        return None

    async def chat_stream(
        self, 
        messages: List[Dict[str, Any]], 
        temperature: float = 0.7
    ) -> AsyncIterator[str]:
        """Stream chat completions with proper SSE format"""
        try:
            callback_handler = AsyncIteratorCallbackHandler()
            llm = ChatOpenAI(
                streaming=True,
                callbacks=[callback_handler],
                temperature=temperature,
                model=self.model_name,
                openai_api_key=self.api_key
            )

            current_chunk = []
            full_response = []
            
            # Send start message
            yield self.format_sse("start", "Starting response...")
            
            async for chunk in llm.astream(messages):
                if hasattr(chunk, 'content'):
                    token = chunk.content
                    current_chunk.append(token)
                    full_response.append(token)
                    
                    # Try to accumulate meaningful chunks
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
        messages: List[Dict[str, Any]], 
        temperature: float = 0.7
    ) -> str:
        """Get single chat completion response"""
        try:
            llm = ChatOpenAI(
                streaming=False,
                temperature=temperature,
                model=self.model_name,
                openai_api_key=self.api_key
            )
            response = await llm.ainvoke(messages)
            return response.content
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")