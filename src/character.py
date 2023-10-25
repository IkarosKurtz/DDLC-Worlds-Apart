from src.character_logging import CustomLogger
from character_data import CharacterDetails
from agent_memory_manager import AgentMemoryManager
from .agent_memory.agent_memory import AgentMemory
from .agent_memory.generative_memory import GenerativeAgentMemory
from .agent_memory.memory import MemoryEntry
from .decision_making.thread_decorator import create_thread
from .openai_helpers.chat_completion import chat_completion
from dotenv import load_dotenv

import time
import threading
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
      saved_status  = self._generate_status() 
    
    self._character_data = CharacterDetails(name, bio, traits, habilites, saved_status, 'club room')
    
    self._logger = CustomLogger(self._personal_data)
    
    memories = [memory.strip() for memory in memories.split(';')]
    
    self._conversation_history = []

    initial_time = time.time()
        
    self._agent_memory = AgentMemory(memories, self._character_data, self._logger, self._memory_db)
    
    self._generative_memory = GenerativeAgentMemory(self._character_data, self._agent_memory, self._logger)
  
    self._character_data.bio = self._generate_bio()
    
    # Program a way to update the status every 5 minutes
    
    self._generate_bio_thread = threading.Thread(target=self._generate_bio, daemon=True, name='Generate Bio Thread')
    
    if self._agent_memory._is_initial_run:
      self._generative_memory.generate_reflections()
      
    self._logger.agent_info(f'Finished initializing character in {time.time() - initial_time} seconds')
    
  @property
  def character_data(self) -> CharacterDetails:
    return self._character_data
  
  @property
  def memories(self) -> list[MemoryEntry]:
    return self._agent_memory.memories
    
  def _generate_bio(self) -> str:
    self._logger.agent_info('Generating bio...')

    questions = (
      f'Key features of {self._character_data.name}, what makes it unique.',
      f'Current daily occupation of {self._character_data.name}.',
      f'How is {self._character_data.name} feeling about their recent progress in life.'
    )

    prompts = (
      textwrap.dedent("""
      How would one describe the key features of {} given the following statements?
      Use a maximum of 120 words. Include only the summary, do not add a title or the like.

      Only use the information provided below:
      {}
      """),
      textwrap.dedent("""
      How would one describe the daily occupation of {} given the following statements?
      Use a maximum of 120 words. Include only the summary, do not add a title or the like.

      Only use the information provided below:
      {}
      """),
      textwrap.dedent("""
      How would one describe the recent progress in {}'s life given the following statements?
      Use a maximum of 120 words. Include only the summary, do not add a title or the like.

      Only use the information provided below:
      {}
      """)
    )

    @create_thread
    def generate_summary(prompt: str, question: str) -> str:
      memories = self._generative_memory.retrieve(question)

      list_of_memories = '\n'.join([f'- {memory.access()}.' for memory in memories])

      summary, _ = chat_completion(prompt.format(self._character_data.name, list_of_memories))
      
      self._logger.agent_info(f'Generated summary for {question}\nSummary: {summary}')

      return summary
    
    threads = [generate_summary(prompt, question) for prompt, question in zip(prompts, questions)]
      
    summaries = [thread.result() for thread in threads]

    new_description = textwrap.dedent("""
    You are a person named {}.
    Your bio is the following:
    {}
    
    Your habilites are the following:
    {}
    
    Your traits are the following:
    {}    
    """).format(self._character_data.name, '\n\n'.join(summaries), self._traits)

    self._logger.agent_info(f'Generated bio: {new_description}')

    return new_description
    
  def _generate_status(self) -> str:
    self._logger.agent_info('Generating status...')
    
    recent_memories = self._agent_memory.memories[:30]
  
    list_of_memories = '\n'.join([f'{i + 1}. {memory.access()}' for i, memory in enumerate(recent_memories)])

    prompt = textwrap.dedent("""
    Información (Records):
    {}

    ¿Cual seria el estado emocional actual de {} dadas las afirmaciones de arriba?
    Utiliza como máximo 10 palabras y de forma OBLIGATORIA utiliza el formato de abajo.
                            
    El resultado debe estar en 3ra persona aclarando quien es la persona a la que se refiere.

    Formato:
    Status: <FILL IN>
    """).format(list_of_memories, self._character_data.name)

    new_status, _ = chat_completion(prompt)

    new_status = new_status.split(':')[1].strip()

    self._logger.agent_info(f'Generated new_status: {new_status}')

    self._memory_db.set_agent_status(new_status)

    return new_status