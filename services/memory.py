from letta import create_client, LLMConfig, EmbeddingConfig
from letta.schemas.memory import ChatMemory, BasicBlockMemory
from core.config import OPENAI_MODEL, OLLAMA_MODEL
class MemoryService:
    def __init__(self):
        """Initialize letta client"""
        self.letta_client = create_client()
        
    def create_agent(self, persona: str):
        """Create a new agent with the given persona, returns agent state"""
        
        persona_block = self.letta_client.create_block(
			label="persona",
			value="I am Yara, your personal beauty assistant, answer all question related to lifestyle, beauty, skin, looks and style",
			limit=1000
		)
        return self.letta_client.create_agent(
			memory=BasicBlockMemory(
				blocks=[persona_block]
			),
			llm_config=LLMConfig.default_config(
				model_name=OPENAI_MODEL
			),
			embedding_config=EmbeddingConfig.default_config(
				model_name="text-embedding-ada-002"
			)
		)
    
    def create_block_memory(self):
        """Create a new block memory"""
        
        persona_block = self.letta_client.create_block(
			label="persona",
			value="I am a beauty assistant, answer all question related to lifestyle, beauty, skin, looks and style",
			limit=1000
		)