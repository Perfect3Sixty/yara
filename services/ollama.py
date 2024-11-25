# services/ollama.py
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import AsyncIterator, Dict, Any, List
import asyncio
import uuid
from datetime import datetime

class OllamaService:
    def __init__(self, base_url: str, model_name: str):
        self.base_url = base_url
        self.model_name = model_name
        self.embeddings = OllamaEmbeddings(
            base_url=base_url,
            model=model_name
        )

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
            return f"data: {json_data}\n\n"
        
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
            llm = Ollama(
                base_url=self.base_url,
                model=self.model_name,
                streaming=True,
                callbacks=[callback_handler],
                temperature=temperature
            )

            current_chunk = []
            full_response = []
            
            # Send start message
            yield self.format_sse("start", "Starting response...")
            
            # Convert messages to prompt format that Ollama expects
            prompt = self._convert_messages_to_prompt(messages)
            
            async for chunk in llm.astream(prompt):
                if chunk:
                    token = chunk
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

    def _convert_messages_to_prompt(self, messages: List[Dict[str, Any]]) -> str:
        """Convert chat messages to Ollama prompt format"""
        prompt_parts = []
        for message in messages:
            role = message["role"]
            content = message["content"]
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
            
        return "\n".join(prompt_parts)

    async def chat_completion(
        self, 
        messages: List[Dict[str, Any]], 
        temperature: float = 0.7
    ) -> str:
        """Get single chat completion response"""
        try:
            llm = Ollama(
                base_url=self.base_url,
                model=self.model_name,
                streaming=False,
                temperature=temperature
            )
            
            # Convert messages to prompt format
            prompt = self._convert_messages_to_prompt(messages)
            
            response = await llm.ainvoke(prompt)
            return response
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")