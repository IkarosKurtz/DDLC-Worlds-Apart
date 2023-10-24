from src.character_logging import CustomLogger
from character_data import CharacterDetails
from agent_memory_manager import AgentMemoryManager
from .agent_memory.agent_memory import AgentMemory
from dotenv import load_dotenv
import os
import openai
load_dotenv()

openai.api_key = os.getenv("OPENAI")

class Character:
  def __init__(self, name: str, bio: str, habilites: str, memories: str, traits: str) -> None:
    self._database = AgentMemoryManager(name, 'json')

    saved_status = self._database.get_agent_status()
    
    if saved_status is None:
      # Generate new status
      pass
    else:
      self._status = saved_status    
    
    self._personal_data = CharacterDetails(name, bio, traits, habilites, saved_status, 'chat')
    
    self._character_logger = CustomLogger(self._personal_data)
    
    memories = [memory.strip() for memory in memories.split(';')]
    
    self._memory_stream = AgentMemory(memories, self._personal_data, self._character_logger, self._database)