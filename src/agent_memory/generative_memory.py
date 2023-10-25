from ..openai_helpers.chat_completion import chat_completion
from ..decision_making.thread_decorator import create_thread
from ..agent_memory.agent_memory import AgentMemory
from ..character_data import CharacterDetails
from ..character_logging import CustomLogger
from ..agent_memory.memory import MemoryEntry, MemoryKind
from openai.embeddings_utils import get_embedding, cosine_similarity

import textwrap
import re

class GenerativeAgentMemory:
  def __init__(self, character_data: CharacterDetails, agent_memory: AgentMemory, logger: CustomLogger) -> None:
    self._character_data = character_data
    self._agent_memory = agent_memory
    self._logger = logger

  def _create_query_questions(self) -> list[str]:
    self._logger.agent_info('Creating query questions...')
    memories = self._agent_memory.memories[:70]
    formatted_memories = '\n'.join([f'{i + 1}. {memory.access()}' for i, memory in enumerate(memories)])

    prompt = textwrap.dedent("""
    Information (Records):
    {}

    Taking into account only the information above,
    What are the top 3 high-level questions we can answer about the topics mentioned? (ONLY WRITE THE QUESTIONS, NOT THE ANSWERS)

    Format:
    Question 1: <FILL IN>
    Question 2: <FILL IN>
    Question 3: <FILL IN>
    """).format(formatted_memories)

    query_questions, _ = chat_completion(prompt, 'You are good at deducing things from statements, you always answer in a concrete, brief and easy to understand way.')
    formatted_questions = [question.split(':')[1].strip() for question in query_questions.strip().split('\n')]

    self._logger.agent_info('Finished creating query questions')
    
    for question in formatted_questions:
      self._logger.agent_info(f'Question: {question}')

    return formatted_questions

  @create_thread
  def _generate_reflection(self, memory_query: str) -> list[dict]:
    normalized_query = memory_query.strip()
    memories = self.retrieve(normalized_query)
    formatted_memories = '\n'.join([f'{i + 1}. {memory.access()}' for i, memory in enumerate(memories)])

    prompt = textwrap.dedent("""
    Statements about {}
    {}

    Using only the information provided above,
    What 5 high-level ideas can you deduce from the statements above?
    Use a maximum of 20 words per idea (references do not count toward the maximum word count).

    It is MANDATORY to follow the following format, there must always be references to the memories that generated the reflection, and these must always be enclosed in brackets, even if it's just a single reference:

    Format:
    1. <Insight>. /*/ References: [<FILL IN>]
    2. <Insight>. /*/ References: [<FILL IN>]
    3. <Insight>. /*/ References: [<FILL IN>]
    """)

    insights, _ = chat_completion(prompt.format(self._character_data.name, formatted_memories), 'Eres un asistente util y haces lo que te piden al pie de la letra.')

    new_reflections = []
    for insight in insights.strip().split('\n'):
      description, refs = insight.split('/*/')
      references = [int(ref) for ref in re.findall(r"\d+", refs)]
      memory_references = [memories[ref - 1].id for ref in references]
      new_reflections.append({'description': description.strip(), 'references': memory_references})

    return new_reflections

  @create_thread
  def _save_memory(self, memory: dict) -> None:
    try:
      self._agent_memory.record_memory(memory['description'], MemoryKind.REFLECTION, memory['references'])
    except Exception as e:
      self._logger.agent_error(f'Error saving memory: {e}')

  def generate_reflections(self) -> None:
    self._logger.agent_info('Generating reflections...')
    memories_querys = self._create_query_questions()

    new_memories = []
    for memory_query in memories_querys:
      new_memories.extend(self._generate_reflection(memory_query).result())

    for memory in new_memories:
      self._save_memory(memory).result()

  def retrieve(self, query_question: str) -> list[MemoryEntry]:
    recent_memories = self._agent_memory.memories[:70]
    query_embedding = get_embedding(query_question, engine='text-embedding-ada-002')

    for memory in recent_memories:
      recency = memory.calculate_recency()
      importance = memory.importance
      relevance = cosine_similarity(query_embedding, memory.embedding)

      recency_normalized = recency / 1
      importance_normalized = (importance - 1) / 9
      relevance_normalized = relevance / 1

      memory.retrieval_value = (recency_normalized + importance_normalized + relevance_normalized)

    recent_memories.sort(key=lambda memory: memory.retrieval_value, reverse=True)
    
    return recent_memories