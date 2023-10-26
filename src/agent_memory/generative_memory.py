from ..openai_helpers.chat_completion import chat_completion
from ..decision_making.thread_decorator import threaded
from ..agent_memory.agent_memory import AgentMemory
from ..character_data import CharacterDetails
from ..custom_logger import CustomLogger
from ..agent_memory.memory import MemoryKind

import textwrap
import re


class GenerativeAgentMemory:
  """ A class responsible for enhancing an agent's memory by generating reflections based on stored memories. """

  def __init__(self, character_data: CharacterDetails, agent_memory: AgentMemory, logger: CustomLogger) -> None:
    """
    Initializes the GenerativeAgentMemory with character data, agent memory, and logger.

    Parameters
    ----------
    character_data : CharacterDetails
        Character data for the agent.

    agent_memory : AgentMemory
        Memory manager of the agent.

    logger : CustomLogger
        Logger for the agent.
    """
    self._character_data = character_data
    self._agent_memory = agent_memory
    self._logger = logger

  def _create_query_questions(self) -> list[str]:
    """
    Creates high-level query questions based on the agent's memories.

    Returns
    -------
    list[str]
        A list of high-level query questions.
    """
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

    query_questions, _ = chat_completion(
      prompt, 'You are good at deducing things from statements, you always answer in a concrete, brief and easy to understand way.')
    formatted_questions = [question.split(':')[1].strip() for question in query_questions.strip().split('\n')]

    self._logger.agent_info('Finished creating query questions')

    for question in formatted_questions:
      self._logger.agent_info(f'Question: {question}')

    return formatted_questions

  @threaded
  def _generate_reflection(self, memory_query: str) -> list[dict]:
    """
    Generates reflections based on a specific memory query.

    Parameters
    ----------
    memory_query : str
        A high-level query to generate reflections.

    Returns
    -------
    list[dict]
        A list of reflections, each as a dictionary containing description and references.
    """
    normalized_query = memory_query.strip()
    memories = self._agent_memory.retrieve(normalized_query)
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
    """).format(self._character_data.name, formatted_memories)

    insights, _ = chat_completion(prompt)

    new_reflections = []
    for insight in insights.strip().split('\n'):
      description, refs = insight.split('/*/')
      references = [int(ref) for ref in re.findall(r"\d+", refs)]
      memory_references = [memories[ref - 1].id for ref in references]
      new_reflections.append({'description': description.strip(), 'references': memory_references})

    return new_reflections

  @threaded
  def _save_memory(self, memory: dict) -> None:
    """
    Saves a generated memory (reflection) into the agent's memory.

    Parameters
    ----------
    memory : dict
        A dictionary containing the description and references of a memory.
    """
    try:
      self._agent_memory.record_memory(memory['description'], MemoryKind.REFLECTION, memory['references'])
    except Exception as e:
      self._logger.agent_error(f'Error saving memory: {e}')

  def generate_reflections(self) -> None:
    """
    Generates and saves reflections based on the agent's memories.
    """
    self._logger.agent_info('Generating reflections...')
    memory_queries = self._create_query_questions()

    threads = [self._generate_reflection(memory_query) for memory_query in memory_queries]
    reflections = [thread for thread in threads]

    save_threads = []

    for reflection in reflections:
      for memory in reflection:
        save_threads.append(self._save_memory(memory))
