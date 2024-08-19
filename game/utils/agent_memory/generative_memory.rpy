init -998 python:
  import textwrap
  import re


  class GenerativeAgentMemory:
    """ A class responsible for enhancing an agent's memory by generating reflections based on stored memories. """

    def __init__(self, agent_details: AgentDetails, memory_stream: MemoryStream, memory_db: JSONDatabase, logger: CustomLogger) -> None:
      """
      Initializes the GenerativeAgentMemory with character data, agent memory, and logger.

      Parameters
      ----------
      agent_details : AgentDetails
          Character data for the agent.

      memory_stream : MemoryStream
          The memory stream of the agent.

      logger : CustomLogger
          Logger for the agent.
      """
      self._agent_details = agent_details
      self._memory_stream = memory_stream
      self._logger = logger
      self._memory_db = memory_db

      self.insight_pattern = re.compile(r'^.*Insight.*$', re.MULTILINE)
      self.question_pattern = re.compile(r'^.*Question.*$', re.MULTILINE)

    def _generate_query_questions(self) -> list[str]:
      """
      Creates high-level query questions based on the agent's memories.

      Returns
      -------
      list[str]
          A list of high-level query questions.
      """
      self._logger.agent_info('Creating query questions...')
      memories = self._memory_stream.memories[:70]
      formatted_memories = '\n'.join([f'{i + 1}. {memory.access()}' for i, memory in enumerate(memories)])

      prompt = textwrap.dedent("""
      Information (Records):
      {}

      Give me 3 high-level questions about the above information. Just give me the questions, don't give me the answers.

      Fill In, don't write anything else:
      Question 1: <QUESTION>
      Question 2: <QUESTION>
      Question 3: <QUESTION>
      """).format(formatted_memories)

      query_questions, _ = chat_completion(
        prompt, 'You are good at deducing things from statements, you always answer in a concrete, brief and easy to understand way.', temperature=0.1)

      print(f"Query questions: {query_questions}")

      questions = self.question_pattern.findall(query_questions)
      questions = [question.strip().split(":")[1].strip() for question in questions]

      print(questions)

      self._logger.agent_info('Finished creating query questions')

      for question in questions:
        self._logger.agent_info(f'Question: {question}')

      return questions

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
      memories = self._memory_stream.retrieve(normalized_query)
      formatted_memories = '\n'.join([f'{i + 1}. {memory.access()}' for i, memory in enumerate(memories)])

      prompt = textwrap.dedent("""
      Statements about {}
      {}

      Using only the information provided above,
      What 5 high-level ideas can you deduce from the statements above?
      Use a maximum of 20 words per idea (references do not count toward the maximum word count).

      It is MANDATORY to follow the following format, there must always be references to the memories that generated the reflection, and these must always be enclosed in brackets, even if it's just a single reference and need to be with numbers:

      Examples:
      Insight 1: The weather is sunny today. /*/ [1, 2, 3]
      Insight 2: Today it was a moving day. /*/ [6]
      Insight 3: My friend is a great person. /*/ [2, 5]

      Format, do not write anything else:
      Insight 1: <Insight>. /*/ <NumberedReferences>
      Insight 2: <Insight>. /*/ <NumberedReferences>
      Insight 3: <Insight>. /*/ <NumberedReferences>
      Insight 4: <Insight>. /*/ <NumberedReferences>
      Insight 5: <Insight>. /*/ <NumberedReferences>
      """).format(self._agent_details.name, formatted_memories)

      insights, _ = chat_completion(prompt, "you are a helpful assistant, uou follow the format of the prompt, and you are not allowed to write anything else, just the insights, and the references", temperature=0.1)

      print(prompt)

      insights = self.insight_pattern.findall(insights)
      insights = [insight.strip().split(':')[1].strip() for insight in insights]

      generated_reflections = []

      def wrap(insight: str) -> None:
        insight = insight.strip()
        if insight == '':
          return

        self._logger.memory_info(f"Insight: {insight}")
        description, refs = insight.split('/*/')
        references = [int(ref) for ref in re.findall(r"\d+", refs.strip())]
        memory_references = [memories[ref - 1]._id for ref in references]

        generated_reflection = self._memory_stream.generate_memory(description.strip(), MemoryType.REFLECTION, memory_references)

        generated_reflections.append(generated_reflection)

      futures = [executor.submit(wrap, insight) for insight in insights]
      _ = [future.result() for future in futures]

      return generated_reflections

    def generate_reflections(self) -> None:
      """
      Generates and saves reflections based on the agent's memories.
      """
      self._logger.both_info('Generating reflections...')
      memory_queries = self._generate_query_questions()

      futures = [executor.submit(self._generate_reflection, memory_query) for memory_query in memory_queries]
      reflections = []

      for future in futures:
        result = future.result()
        reflections.extend(result)

      self._memory_stream._all_memories.extend(reflections)
      self._memory_db.store_memories([m.as_dict() for m in reflections])

      self._logger.both_info(f"Generated {len(reflections)} memories")




