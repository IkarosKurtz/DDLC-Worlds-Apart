init -999 python:
  from enum import Enum
  import datetime
  import math
  from dataclasses import dataclass, field
  from typing import Optional

  class MemoryType(Enum):
    """
    Enumeration for kinds of memory entries.

    Attributes
    ----------
    OBSERVATION : int
        Represents an observational memory.
    REFLECTION : int
        Represents a reflective memory.
    """

    OBSERVATION = 0
    REFLECTION = 1


  @dataclass
  class MemoryEntry:
    description: str
    importance: int
    memory_type: MemoryType

    _id: float = field(default_factory=lambda: datetime.datetime.now().timestamp())
    created_at: float = field(default_factory=lambda: datetime.datetime.now().timestamp())
    accessed_at: float = field(default_factory=lambda: datetime.datetime.now().timestamp())
    retrieval_value: float = 0.0
    embedding: Optional[list[float]] = field(default=None)
    associated_memories: list[float] = field(default_factory=list)

    def __post_init__(self):
      if self.embedding is None:
        self.embedding = get_embedding(self.description)

    def access(self) -> str:
      """
      Updates the accessed timestamp and returns the description of the memory.

      Returns
      -------
      str
          The description of the memory.
      """
      self.accessed_at = datetime.datetime.now().timestamp()
      return self.description

    def calculate_recency(self) -> float:
      """
      Calculates and returns the recency/decay value of the memory.

      Returns
      -------
      float
          The recency/decay value of the memory.
      """
      diff = datetime.datetime.now().timestamp() - self.accessed_at
      self.access()

      recency = math.pow(.99, diff / 3600)  # diff in milliseconds
      return recency

    def as_dict(self) -> dict:
      """
      Returns a dictionary representation of the memory entry.

      Returns
      -------
      dict
          A dictionary containing key details of the memory entry.
      """
      return {
        '_id': self._id,
        'memory_type': self.memory_type.name,
        'description': self.description,
        'retrieval_value': self.retrieval_value,
        'importance': self.importance,
        'associated_memories': self.associated_memories,
        'created_at': self.created_at,
        'accessed_at': self.accessed_at,
        'embedding': self.embedding
      }
