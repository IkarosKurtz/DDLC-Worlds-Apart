init -999 python:
  import textwrap
  import re

  class MemoryStream:
    """ Manages the agent's memory stream. """

    def __init__(self, initial_memories: list[str], agent_details: AgentDetails, logger: CustomLogger, memory_db: AgentMemoryManager) -> None:
      """
      Initialize the MemoryStream with initial memories, character data, logger, and memory database manager.

      Parameters
      ----------
      initial_memories : list[str]
          List of initial memories as strings to load into the agent's memory.

      agent_details : AgentDetails
          Character data containing information about the agent.

      logger : CustomLogger
          Logger to log information related to the agent's activities.

      memory_db : AgentMemoryManager
          Database manager for storing and retrieving memories.
      """
      self._agent_details = agent_details
      self._logger = logger
      self._memory_db = memory_db

      self._all_memories: list[MemoryEntry] = []
      self._is_initial_run: bool = True

      self._logger.both_info("Initializing memories")

      # Save only the memories that are not already in the database
      filtered_initial_memories = [m for m in initial_memories if self._memory_db.retrieve_memory(m) is None]

      self._logger.memory_info(f"Filtered initial memories: {len(filtered_initial_memories)}")

      if len(filtered_initial_memories) == 0:
        self._is_initial_run = False
        self._logger.both_info(f"Initial memories already initialized")

      if len(filtered_initial_memories) > 0:
        futures = [
          executor.submit(self.generate_memory, filtered_initial_memories[i])
          for i in range(0, len(filtered_initial_memories))
        ]
        memories = [future.result() for future in futures]

        self._all_memories.extend(memories)
        self._memory_db.store_memories([memory.as_dict() for memory in memories])
        
        self._logger.both_info(f"Initialized {len(self._all_memories)} memories")


      memories_descriptions = [m.description for m in self._all_memories]

      saved_memories = self._memory_db.retrieve_all_memories()

      for memory in saved_memories:
        if memory['description'] not in memories_descriptions:
          self._all_memories.append(MemoryEntry(**memory))
          self._logger.both_info(f"Loaded memory: {memory['description']}")

      self._logger.both_info(f"Loaded {len(self._all_memories)} memories")

    @property
    def memories(self) -> list[MemoryEntry]:
      """
      Retrieves all memories sorted by most recent.

      Returns
      -------
      list of MemoryEntry
          A sorted list of memory entries.
      """
      self._all_memories.sort(key=lambda memory: memory.created_at, reverse=True)

      return self._all_memories

    def generate_memory(self, description: str, memory_type: MemoryType = MemoryType.OBSERVATION, associated_memories: list[float] = None) -> None:
      """
      Records a memory in the agent's memory stream.

      Parameters
      ----------
      description : str
          Description of the memory.

      memory_type : MemoryType, optional
          The kind of memory, default is MemoryType.OBSERVATION.

      associated_memories : list[str], optional
          List of associated memories.
      """
      if associated_memories is None:
        associated_memories = []

      prompt = textwrap.dedent("""
      With a one integer rate the significance of the following event on a scale of 1 to 10, where 1 is purely mundane (e.g. brushing teeth, making bed, walking the usual route) and 10 is impactful (e.g., a breakup, college acceptance). Do not include any additional information, only the rating.

      Memory:
      {}

      Fill In:
      <Rating Integer>
      """).format(description.strip())

      importance, _ = chat_completion(prompt, self._agent_details.bio)

      # Just take the first number 
      importance = re.findall(r'\d+', importance)[0]

      self._logger.memory_info(f"Memory > '{description}' > was given a weight of > {importance}")

      importance = float(importance)

      new_memory = MemoryEntry(description, importance, memory_type, associated_memories=associated_memories)

      return new_memory

    def retrieve(self, query_question: str) -> list[MemoryEntry]:
      """
      Retrieves memories relevant to a given query.

      Parameters
      ----------
      query_question : str
          The query question to retrieve memories for.

      Returns
      -------
      list of MemoryEntry
          A sorted list of relevant memory entries.
      """
      recent_memories = self.memories[:70]
      query_embedding = get_embedding(query_question)

      # time_b = time.time()
      for memory in recent_memories:
        recency = memory.calculate_recency()
        importance = memory.importance
        # b_time = time.time()
        relevance = cosine_similarity(query_embedding, memory.embedding)
        # print(f"Cosine similarity calculation took {time.time() - b_time} seconds")

        recency_normalized = recency / 1
        importance_normalized = (importance - 1) / 9
        relevance_normalized = relevance / 1

        memory.retrieval_value = (recency_normalized + importance_normalized + relevance_normalized)

      # print(f"Retrieval value calculation took {time.time() - time_b} seconds")
      recent_memories.sort(key=lambda memory: memory.retrieval_value, reverse=True)

      return recent_memories
