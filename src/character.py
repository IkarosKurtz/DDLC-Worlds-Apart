from src.character_logging import CustomLogger
from character_data import CharacterDetails
from agent_memory_manager import AgentMemoryManager
from .agent_memory.agent_memory import AgentMemory
from .agent_memory.generative_memory import GenerativeAgentMemory
from .decision_making.thread_decorator import create_thread
from .openai_helpers.chat_completion import chat_completion
from dotenv import load_dotenv

import time
import textwrap
import os
import openai
load_dotenv()

openai.api_key = os.getenv("OPENAI")

class Character:
  def __init__(self, name: str, bio: str, habilites: str, memories: str, traits: str) -> None:
    self._memory_db = AgentMemoryManager(name, 'json')

    saved_status = self._memory_db.get_agent_status()
    
    if saved_status is None:
      # Generate new status
      pass
    else:
      self._status = saved_status    
    
    self._character_data = CharacterDetails(name, bio, traits, habilites, saved_status, 'club room')
    
    self._logger = CustomLogger(self._personal_data)
    
    memories = [memory.strip() for memory in memories.split(';')]
    
    self._conversation_history = []

    initial_time = time.time()
        
    self._agent_memory = AgentMemory(memories, self._character_data, self._logger, self._memory_db)