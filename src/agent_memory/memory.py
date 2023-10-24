from enum import Enum
import datetime
import math
import uuid
from openai.embeddings_utils import get_embedding


class MemoryKind(Enum):
    OBSERVATION = 0
    REFLECTION = 1


class Memory:
    def __init__(self, description: str, importance: float, kind: MemoryKind, **attributes) -> None:
        self.description = description
        self.importance = importance
        self.kind = kind
        
        defaults = {
            'id': str(uuid.uuid4()),
            'created_at': datetime.datetime.now(),
            'accessed_at': datetime.datetime.now(),
            'retrieval_value': 0,
            'embedding': get_embedding(description, engine='text-embedding-ada-002'),
            'references': []
        }
        
        for attribute, default in defaults.items():
            setattr(self, f"_{attribute}", attributes.get(attribute, default))

    @property
    def id(self) -> str:
        return self._id

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @property
    def accessed_at(self) -> datetime.datetime:
        return self._accessed_at

    @property
    def retrieval_value(self) -> float:
        return self._retrieval_value

    @retrieval_value.setter
    def retrieval_value(self, value: float) -> None:
        self._retrieval_value = value

    @property
    def embedding(self) -> list[float]:
        return self._embedding

    @property
    def references(self) -> list[str]:
        return self._references

    def access(self) -> None:
        """Update the last accessed time."""
        self._accessed_at = datetime.datetime.now()

    def calculate_recency(self) -> float:
        """Calculate recency of memory based on time since last access."""
        diff = datetime.datetime.now().timestamp() - self._accessed_at.timestamp()
        self.access()
        
        recency = math.pow(.99, diff / 3600) # diff in millisenconds
        return recency

    def as_dict(self) -> dict:
        """Return a dictionary representation of the memory."""
        return {
            '_id': self._id,
            'kind': self.kind.name,
            'description': self.description,
            'retrieval_value': self._retrieval_value,
            'importance': self.importance,
            'references': self._references,
            'created_at': self._created_at,
            'accessed_at': self._accessed_at,
            'embedding': self._embedding
        }
