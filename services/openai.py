# services/openai.py
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from typing import AsyncIterator, Dict, Any, List
import asyncio
import json
from datetime import datetime
import uuid

class OpenAiService:
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    def serialize_messages(self, messages: List[Any]) -> List[Dict[str, str]]:
        """Convert LangChain messages to serializable format"""
        serialized = []
        for msg in messages:
            if isinstance(msg, (SystemMessage, HumanMessage, AIMessage)):
                serialized.append({
                    "role": self._get_role(msg),
                    "content": msg.content
                })
            elif isinstance(msg, dict):
                serialized.append(msg)
            else:
                raise ValueError(f"Unsupported message type: {type(msg)}")
        return serialized

    def _get_role(self, message: Any) -> str:
        """Get the role string for a message"""
        if isinstance(message, SystemMessage):
            return "system"
        elif isinstance(message, HumanMessage):
            return "user"
        elif isinstance(message, AIMessage):
            return "assistant"
        return "unknown"

    async def get_embeddings(self, text: str) -> List[float]:
        """Get embeddings for text"""
        return await asyncio.to_thread(
            self.embeddings.embed_query,
            text
        )

    def format_sse(self, event: str, data: Any) -> str:
        """Format the data as SSE message with event type"""
        json_data = json.dumps(data)
        return f"event: {event}\ndata: {json_data}\n\n"

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

            # Serialize messages before using in function call
            serialized_messages = self.serialize_messages(messages)
            
            # Send start message
            yield self.format_sse("start", {
                "id": f"message-{uuid.uuid4()}",
                "date": datetime.now().isoformat(),
                "message_type": "start",
                "content": "Starting to process your request..."
            })
            
            # Send function call message
            function_call_id = f"call_{uuid.uuid4()}"
            yield self.format_sse("function_call", {
                "id": f"message-{uuid.uuid4()}",
                "date": datetime.now().isoformat(),
                "message_type": "function_call",
                "function_call": {
                    "name": "process_chat",
                    "arguments": json.dumps({"messages": serialized_messages}),
                    "function_call_id": function_call_id
                }
            })
            
            yield self.format_sse("status", {
                "id": f"message-{uuid.uuid4()}",
                "date": datetime.now().isoformat(),
                "message_type": "status",
                "content": "Processing information..."
            })
            yield 'data: [DONE_GEN]\n\n'

            current_chunk = []
            full_response = []
            
            # Use original messages for streaming
            async for chunk in llm.astream(messages):
                if hasattr(chunk, 'content'):
                    token = chunk.content
                    current_chunk.append(token)
                    full_response.append(token)
                    
                    accumulated_text = ''.join(current_chunk)
                    if (token in '.!?\n' and accumulated_text.strip()) or len(accumulated_text) > 150:
                        yield self.format_sse("function_return", {
                            "id": f"message-{uuid.uuid4()}",
                            "date": datetime.now().isoformat(),
                            "message_type": "function_return",
                            "function_return": accumulated_text.strip(),
                            "status": "streaming",
                            "function_call_id": function_call_id
                        })
                        current_chunk = []

            # Send any remaining text
            remaining_text = ''.join(current_chunk).strip()
            if remaining_text:
                yield self.format_sse("function_return", {
                    "id": f"message-{uuid.uuid4()}",
                    "date": datetime.now().isoformat(),
                    "message_type": "function_return",
                    "function_return": remaining_text,
                    "status": "streaming",
                    "function_call_id": function_call_id
                })

            # Send complete response
            complete_response = ''.join(full_response)
            yield self.format_sse("function_return", {
                "id": f"message-{uuid.uuid4()}",
                "date": datetime.now().isoformat(),
                "message_type": "function_return",
                "function_return": complete_response,
                "status": "success",
                "function_call_id": function_call_id
            })
            
            yield 'data: [DONE_STEP]\n\n'
            
            yield self.format_sse("completion", {
                "id": f"message-{uuid.uuid4()}",
                "date": datetime.now().isoformat(),
                "message_type": "completion",
                "content": "Response generated successfully"
            })
            yield 'data: [DONE]\n\n'

        except Exception as e:
            print(f"Error in chat stream: {str(e)}")  # Add debugging
            yield self.format_sse("error", {
                "id": f"message-{uuid.uuid4()}",
                "date": datetime.now().isoformat(),
                "message_type": "error",
                "error": str(e),
                "details": str(getattr(e, '__traceback__', ''))
            })
            yield 'data: [ERROR]\n\n'
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