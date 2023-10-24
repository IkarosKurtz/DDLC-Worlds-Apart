from ..character_data import CharacterDetails
from .memory import Memory, MemoryKind
from ..character_logging import CustomLogger
from typing import Literal as literal
from ..agent_memory_manager import AgentMemoryManager
import textwrap
from ..openai_helpers.chat_completion import chat_completion

class MemoryStream:
  """ Agent memory stream. """
  
  def __init__(self, memories: list[str], personal_data: CharacterDetails, character_logger: CustomLogger, database: AgentMemoryManager) -> None:
    self._personal_data = personal_data
    self._character_logger = character_logger
    self._database = database
    
    self._memories: list[Memory] = []
    
    self._first_run = True
    
    self._character_logger.agent_info(f"Extracting memories")
    
    for memory in memories: # Store Base Memories
      if self._database.retrieve_memory(memory) is None:
        self._first_run = True
        self.store_memory(memory)
        self._character_logger.memory_info(f"Memory: {memory} stored in database")
        
      self._first_run = False
      self._character_logger.memory_info(f"Memory: {memory} already exists in database")
      
    for memory in self._database.retrieve_all_memories():
      self._memories.append(Memory(**memory))
  
  def store_memory(self, memory_description: str, kind: MemoryKind = MemoryKind.OBSERVATION, references: list[str] = None) -> None:
    if references is None: references = []
    
    prompt = textwrap.dedent("""
    On a scale from 1 to 10, where 1 is purely mundane (e.g. brushing your teeth, making the bed, walking the same path)
    and 10 is moving (e.g., a breakup, acceptance into college), rate (based on your perspective) the likely impact of the following memory.
    
    Memory:
    {}
                            
    MANDATORILY, follow the format below, do not explain anything else, just write a single number enclosed in brackets.

    Format:
    Rating: [<FILL IN>]
    """).format(memory_description.strip())
    
    memory_importance, _ = chat_completion(self._personal_data.description, prompt)
    
    self._character_logger
    
    
    
    