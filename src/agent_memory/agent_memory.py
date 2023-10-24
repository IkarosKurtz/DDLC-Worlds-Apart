from ..character_data import CharacterDetails
from .memory import Memory, MemoryKind
from ..character_logging import CustomLogger
from ..agent_memory_manager import AgentMemoryManager
import textwrap
from ..openai_helpers.chat_completion import chat_completion

class AgentMemory:
    """ Manages the agent's memory stream. """
  
    def __init__(self, initial_memories: list[str], character_data: CharacterDetails, logger: CustomLogger, memory_db: AgentMemoryManager) -> None:
        self._character_data = character_data
        self._logger = logger
        self._memory_db = memory_db
        
        self._all_memories: list[Memory] = []
        self._is_initial_run: bool = True
        
        self._logger.agent_info("Initializing memories")
        
        for memory_desc in initial_memories: 
            if self._memory_db.retrieve_memory(memory_desc) is None:
                self._is_initial_run = True
                self.record_memory(memory_desc)
                self._logger.memory_info(f"Stored memory: {memory_desc}")
                
            self._is_initial_run = False
            self._logger.memory_info(f"Memory: {memory_desc} already exists in the database")
        
        for stored_memory in self._memory_db.retrieve_all_memories():
            self._all_memories.append(Memory(**stored_memory))
  
    @property
    def memories(self) -> list[Memory]:
        return self._all_memories
  
    def record_memory(self, description: str, memory_kind: MemoryKind = MemoryKind.OBSERVATION, associated_memories: list[str] = None) -> None:
        if associated_memories is None: 
            associated_memories = []
        
        prompt = textwrap.dedent("""
        On a scale from 1 to 10, where 1 is purely mundane (e.g. brushing teeth, making bed, walking the usual route)
        and 10 is impactful (e.g., a breakup, college acceptance), rate the potential significance of the following memory.

        Memory:
        {}

        STRICTLY follow the given format below; provide only a single integer.

        Format:
        Rating: [<FILL IN>]
        """).format(description.strip())
        
        importance, _ = chat_completion(self._character_data.description, prompt)
        importance = importance.split(':')[1].strip()
        
        self._logger.agent_info(f"Memory '{description}' was given a weight of {importance}")
        
        new_memory = Memory(description, importance, memory_kind, associated_memories=associated_memories)
        
        self._memory_db.store_memory(new_memory.as_dict())
        
        self._all_memories.append(new_memory)
