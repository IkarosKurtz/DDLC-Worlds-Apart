init -998 python:
  import time
  import threading
  import datetime
  import textwrap
  import os

  class Agent:
    """ A character with personal data, memories, and decision-making capabilities. """

    def __init__(self, name: str, bio: str, abilities: str, memories: str, traits: str) -> None:
      """
      Initialize the Character instance with personal data and memories.

      Parameters
      ----------
      name : str
        The name of the character.

      bio : str
        The biography of the character.

      abilities : str
        The abilities or skills of the character.

      memories : str
        The memories of the character, separated by semicolons.

      traits : str
        The traits of the character.

      initial_location : str, optional
        The initial location of the character, by default 'club room'.
      """
      initial_time = time.time()
      self._conversation_history = ''

      self._memory_db = JSONDatabase(name)

      self._agent_details = AgentDetails(name, bio, traits, abilities)

      self._logger = CustomLogger(name)

      initial_memories = [memory.strip() for memory in memories.split(';')]

      self._memory_stream = MemoryStream(initial_memories, self._agent_details, self._logger, self._memory_db)

      self._agent_details.status = self._memory_db.get_agent_status()

      if self._agent_details.status is None or self._agent_details.status == '':
        self._generate_status()

      self._agent_details.bio = self._memory_db.get_agent_bio()

      if self._agent_details.bio is None or self._agent_details.bio == '':
        self._generate_bio()

      self._agent_details.location = self._memory_db.get_agent_location()

      if self._agent_details.location is None or self._agent_details.location == '':
        self._agent_details.location = 'Club Room'
        self._memory_db.set_agent_location(self._agent_details.location)

      self._mood_analyzer = MoodAnalyzer(self._agent_details, self._logger)

      self._decision_processor = DecisionProcessor(self._logger, self._memory_stream, self._agent_details)

      self._generative_memory = GenerativeAgentMemory(self._agent_details, self._memory_stream, self._memory_db, self._logger)

      # self._generate_bio_thread = threading.Thread(target=self._generate_bio, daemon=True, name='Generate Bio Thread')

      if self._memory_stream._is_initial_run:
        self._generative_memory.generate_reflections()

      self._logger.agent_info(f'Finished initializing character in {time.time() - initial_time} seconds \n')

    @property
    def agent_details(self) -> AgentDetails:
      return self._agent_details

    @property
    def memories(self) -> list[MemoryEntry]:
      return self._memory_stream.memories

    def _generate_bio(self) -> str:
      """
      Generate the biography of the character based on its memories and personal data.

      Returns
      -------
      str
        The generated biography of the character.
      """
      self._logger.agent_info('Generating bio...')

      questions = (
        f'Key features of {self._agent_details.name}, what makes it unique.',
        f'Current daily occupation of {self._agent_details.name}.',
        f'How is {self._agent_details.name} feeling about their recent progress in life.'
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

      def generate_summary(args) -> str:
        (prompt, question) = args
        memories = self._memory_stream.retrieve(question)

        list_of_memories = '\n'.join([f'- {memory.access()}.' for memory in memories])

        summary, _ = chat_completion(prompt.format(self._agent_details.name, list_of_memories))

        self._logger.agent_info(f'Generated summary for > {question}\nSummary: {summary}')

        return summary

      futures = [executor.submit(generate_summary, (prompt, question)) for prompt, question in zip(prompts, questions)]
      summaries = [future.result() for future in futures]

      new_description = textwrap.dedent("""
      You are a person named {}.
      Your bio is the following:
      {}
      
      Your abilities are the following:
      {}
      
      Your traits are the following:
      {}    
      """).format(self._agent_details.name, '\n\n'.join(summaries), self._agent_details.abilities, self._agent_details.traits)

      self._logger.agent_info(f'Generated bio: {new_description}')

      self._memory_db.set_agent_bio(new_description)

      self._agent_details.bio = new_description


    def _generate_status(self) -> str:
      """
      Generate the current status of the character based on recent memories.

      Returns
      -------
      str
        The generated status of the character.
      """
      self._logger.agent_info('Generating status...')

      recent_memories = self._memory_stream.memories[:30]

      list_of_memories = '\n'.join([f'{i + 1}. {memory.access()}' for i, memory in enumerate(recent_memories)])

      prompt = textwrap.dedent("""
      Information (Records):
      {}

      What would be the current emotional state of {} based on the statements above?
      Use a maximum of 10 words and follow the format below.

      The result should be in the third person, specifying who the person being referred to is.

      Format:
      Status: <FILL IN>
      """).format(list_of_memories, self._agent_details.name)

      new_status, _ = chat_completion(prompt)

      new_status = new_status.split(':')[1].strip()

      self._logger.agent_info(f'Generated new_status: {new_status}')

      self._memory_db.set_agent_status(new_status)

      self._agent_details.status = new_status
    
    def chat(self, speaker: str, message: str) -> list[list[str]]:
      """
      Engage in a conversation with the character, processing the speaker's message.

      Parameters
      ----------
      speaker : str
        The name of the speaker engaging with the character.

      message : str
        The message or statement made by the speaker.

      Returns
      -------
      tuple(str, str)
        The response and pose of the character.
      """
      initial_time = time.time()

      # print(f'{len(self._memory_stream.memories):_^50}')
      if len(self._memory_stream.memories) % 40 == 0:
        # self._generate_bio_thread.start()
        pass

      self._conversation_history += f'{speaker}: {message.strip()}\n'

      def generate_speaker_action(speaker: str, speaker_message: str) -> str:
        return self._decision_processor.determine_speaker_action(speaker, speaker_message)

      def generate_observation(speaker: str, conversation_history: str) -> str:
        return self._decision_processor.generate_observation(speaker, conversation_history)

      futures = [executor.submit(generate_speaker_action, speaker, message), executor.submit(generate_observation, speaker, self._conversation_history)]
      speaker_action, observation = futures[0].result(), futures[1].result()

      questions = [f'What is the relationship between {self._agent_details.name} and {speaker}?', speaker_action]

      time_b = time.time()
      memory_summaries = self._decision_processor.generate_memory_summaries(questions)
      print(f"Generated memory summaries in {time.time() - time_b} seconds")
      
      # Deprecated
      # posible_action = self._decision_processor.determine_possible_action(observation, memory_summaries)

      self._logger.agent_info(f'Generating response...')

      prompt = textwrap.dedent("""
      Current Date: {}
      {} State: {}
      Current Location: {}

      Observation:
      {}

      Summary of {} and their relationship with {}:
      {}

      What should {} say? Remember to use only the information provided to you.

      Below is the conversation history up to this point:
      {}
      
      Format:
      Response: <FILL IN>
      """).format(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        f"{self._agent_details.name}'s" if not self._agent_details.name.endswith('s') else f"{self._agent_details.name}'",
        self._agent_details.status,
        self._agent_details.position,
        observation,
        self._agent_details.name,
        speaker,
        '\n\n'.join([summary for summary in memory_summaries]),
        # posible_action,
        self._agent_details.name,
        self._conversation_history
      )

      self._logger.agent_info(f'Generated prompt: {prompt}')

      response, tokens = chat_completion(prompt, self._agent_details.bio, temperature=0.8)
      response = response[response.find(':') + 1:].strip()
      response = response.replace("\"", "")

      self._logger.agent_info(f'Generated response: {response} Tokens: {tokens}')

      self._conversation_history += f'{self._agent_details.name}: {response}\n'
      
      time_b = time.time()
      response_chunks = [m.strip() if m.endswith('?') or m.endswith('!') else m.strip() + '.' for m in response.split('.') if m.strip() != '']
      
      futures = [executor.submit(self._mood_analyzer.determine_pose, chunk) for chunk in response_chunks]

      poses = [future.result() for future in futures]

      full_response = [[pose, chunk] for pose, chunk in zip(poses, response_chunks)]
      
      print(f"Generated full response in {time.time() - time_b} seconds")

      persistent.current_tokens = tokens
      
      if tokens > 3000:
        self._conversation_history = ''
        self._generative_memory.generate_reflections()

      memory = self._memory_stream.generate_memory(observation)

      self._memory_stream._all_memories.append(memory)
      self._memory_db.store_memory(memory.as_dict())

      self._logger.agent_info(f'Finished generating response in {time.time() - initial_time} seconds \n')

      return full_response