init -999 python:
  import textwrap
  import datetime

  class DecisionProcessor:
    """ Processes decision-making for generic questions, reasoning, and planning. """

    def __init__(self, logger: CustomLogger, memory_stream: MemoryStream, agent_details: AgentDetails) -> None:
      """
      Initializes the DecisionProcessor.

      Parameters
      ----------
      logger : CustomLogger
          An instance of CustomLogger for logging information.

      memory_stream : MemoryStream
          An instance of MemoryStream for retrieving and storing memories.

      agent_details : AgentDetails
          An instance of AgentDetails containing details about the character.
      """
      self._memory_stream = memory_stream
      self._agent_details = agent_details
      self._logger = logger

    def generate_observation(self, speaker: str, conversation: str) -> str:
      """
      Generates a high-level observation about the conversation.

      Parameters
      ----------
      speaker : str
          The name of the speaker.

      conversation : str
          The content of the conversation.

      Returns
      -------
      str
          The generated high-level observation about the conversation.
      """
      self._logger.agent_info('Generating observation...')

      prompt = textwrap.dedent("""
      Conversation between {} and {}:
      {}

      Location: {}

      Using only the information above,
      What high-level observation can be generated about the conversation (do not infer anything)? Describe the observation in a sentence and do not omit important information.

      Use a maximum of 45 words and minimum of 10 words, and MANDATORY use the format below.

      Format:
      Observation: <FILL IN>
      """).format(speaker, self._agent_details.name, conversation, self._agent_details.position)
      time_b = time.time()
      observation, _ = chat_completion(prompt)

      observation = observation.split(':')[1].strip()

      self._logger.agent_info(f'Generated observation: {observation} in {time.time() - time_b} seconds')

      return observation

    def generate_memory_summaries(self, questions: list[str]) -> list[str]:
      """
      Generates summaries of memories related to given questions.

      Parameters
      ----------
      questions : list[str]
          A list of questions for which memory summaries are to be generated.

      Returns
      -------
      list[str]
          A list of generated memory summaries.
      """
      self._logger.agent_info('Generating memory summaries...')

      prompt = textwrap.dedent("""
      Information (Records):
      {}

      Using only the information above.
      Make an exact summary that is coherent, concise, and complete with a maximum of 130 words and minimum of 50 words. Only put the summary, no titles or things like that.
      MANDATORY, follow the following format:

      Format:
      Summary: <FILL IN>
      """)

      summaries = []

      def wrap(question: str) -> None:
        time_b = time.time()
        memories_retrieved = self._memory_stream.retrieve(question)
        memories_descriptions = '\n'.join([f'{i + 1}. {memory.access()}' for i, memory in enumerate(memories_retrieved)])
        summary, _ = chat_completion(prompt.format(memories_descriptions))
        normalized_summary = summary.split(':')[1].strip()

        self._logger.agent_info(f'Generated memory summary: {normalized_summary} in {time.time() - time_b} seconds')

        summaries.append(normalized_summary)

      futures = [executor.submit(wrap, question) for question in questions]
      _ = [future.result() for future in futures]
      
      return summaries

    def determine_speaker_action(self, speaker: str, speaker_message: str) -> str:
      """
      Determines the high-level action taken by a speaker in a conversation.

      Parameters
      ----------
      speaker : str
          The name of the speaker.

      speaker_message : str
          The message or content spoken by the speaker.

      Returns
      -------
      str
          The high-level action taken by the speaker.
      """
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
      """).format(speaker, self._agent_details.name, f'{speaker}: {speaker_message}', speaker)

      time_b = time.time()
      speaker_action, _ = chat_completion(prompt)

      speaker_action = speaker_action.split(':')[1].strip()

      self._logger.agent_info(f'Determined speaker action: {speaker_action} in {time.time() - time_b} seconds')

      return speaker_action


    def determine_possible_action(self, observation: str, memory_summaries: list[str]) -> str:
      """
      Determines a possible action the agent can take based on the observation and memory summaries.

      Deprecated
      ----------
          Because the agent is not able to move (yet) and this is not needed.

      Parameters
      ----------
      observation : str
          The high-level observation about the situation.

      memory_summaries : list[str]
          A list of summaries of relevant memories.

      Returns
      -------
      str
          The determined possible action for the agent.
      """
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
        self._agent_details.name,
        self._agent_details.bio,
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        self._agent_details.name,
        self._agent_details.status,
        self._agent_details.position,
        observation,
        self._agent_details.name,
        '\n\n'.join([f'{summary}' for summary in memory_summaries]),
        self._agent_details.name
      )

      possible_action, _ = chat_completion(prompt, self._agent_details.bio)

      possible_action = self._prev_possible_action = possible_action.split(':')[1].strip()

      self._logger.agent_info(f'Generated possible agent action: {possible_action}')

      return possible_action
