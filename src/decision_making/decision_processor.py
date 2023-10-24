from ..agent_memory.agent_memory import AgentMemory
from ..character_data import CharacterDetails
from ..character_logging import CustomLogger
from ..openai_helpers.chat_completion import chat_completion
from .thread_decorator import create_thread
import textwrap
import datetime

class DecisionProcessor:
  """Processes decision-making for generic questions, reasoning, and planning."""

  def __init__(self, logger: CustomLogger, agent_memory: AgentMemory, character_data: CharacterDetails) -> None:
    self._agent_memory = agent_memory
    self._character_data = character_data
    self._logger = logger
  
  def determine_speaker_action(self, speaker: str, speaker_message: str) -> str:
    self._logger.agent_info(f'Determining speaker action for {speaker}...')

    prompt = textwrap.dedent("""
    Conversation between {} and {}:
    {}

    Using only the information above,
    What high-level action is {} taking? Describe the action in a sentence.
    Use a maximum of 20 words and MANDATORY use the format below.

    The result must be in 3rd person clarifying who the person is.

    Format:
    Action: <FILL IN>
    """).format(speaker, self._character_data.name, f'{speaker}: {speaker_message}', speaker)

    speaker_action, _ = chat_completion('You are a helpful assistant.', prompt)

    speaker_action = speaker_action.split(':')[1].strip()

    self._logger.agent_info(f'Determined speaker action: {speaker_action}')

    return speaker_action

  def generate_observation(self, speaker: str, conversation: str) -> str:
    self._logger.agent_info('Generating observation...')

    prompt = textwrap.dedent("""
    Conversation between {} and {}:
    {}

    Location: {}

    Using only the information above,
    What high-level observation can be generated about the conversation (do not infer anything)? Describe the observation in a sentence and do not omit important information.

    Use a maximum of 40 words and MANDATORY use the format below.

    Format:
    Observation: <FILL IN>
    """).format(speaker, self._character_data.name, conversation, self._character_data.location)

    observation, _ = chat_completion('You are a helpful assistant.', prompt)

    observation = observation.split(':')[1].strip()

    self._logger.agent_info(f'Generated observation: {observation}')

    return observation

  def generate_memory_summaries(self, questions: list[str]) -> list[str]:
    self._logger.agent_info('Generating memory summaries...')
  
    prompt = textwrap.dedent("""
    Information (Records):
    {}

    Using only the information above.
    Make an exact summary that is coherent, concise, and complete. Only put the summary, no titles or things like that.
    MANDATORY, follow the following format (the summary has to be in Spanish):

    Format:
    Summary: <FILL IN>
    """)

    summaries = []

    @create_thread
    def wrap(question: str) -> None:
      memories_retrieved = self._agent_memory.retrieve(question)
      memories_descriptions = '\n'.join([f'{i + 1}. {memory.access()}' for i, memory in enumerate(memories_retrieved)])
      summary, _ = chat_completion('You are a helpful assistant.', prompt.format(memories_descriptions))
      normalized_summary = summary.split(':')[1].strip()

      self._logger.agent_info(f'Generated memory summary: {normalized_summary}')

      summaries.append(normalized_summary)
        
    threads = [wrap(question) for question in questions]
        
    for thread in threads:
      thread.result()
    
    return summaries

  def generate_possible_agent_action(self, observation: str, memory_summaries: list[str]) -> str:
    self._logger.agent_info('Generating possible agent action...')
    
    prompt = textwrap.dedent("""
    Description of {}:
    {}
    Current date: {}
    State of {}: {}
    Location: {}

    Observation:
    {}

    Relevant context summary of {}'s memory:
    {}

    Should {} react to the observation? And if so, how should they react to the observation?
    Use a maximum of 10 words and MANDATORY use the format below.
    Do not use information that was not given to you.

    Format:
    Action: <FILL IN>
    """).format(
    self._character_data.name,
    self._character_data.description,
    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    self._character_data.name,
    self._character_data.status,
    self._character_data.location,
    observation,
    self._character_data.name,
    '\n\n'.join([f'{summary}' for summary in memory_summaries]),
    self._character_data.name
    )

    possible_action, _ = chat_completion(self._character_data.description, prompt)

    possible_action = self._prev_possible_action = possible_action.split(':')[1].strip()

    self._logger.agent_info(f'Generated possible agent action: {possible_action}')

    return possible_action