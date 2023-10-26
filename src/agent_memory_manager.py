from dotenv import load_dotenv
from pymongo import MongoClient
from typing import Literal as literal

import os
import json
import datetime
import dateutil.parser


class AgentMemoryManager:
  """ A class to manage an agent's memory, enabling storage and retrieval of memories and status. """

  def __init__(self, agent_name: str, storage_mode: literal["mongodb", "json"] = "mongodb"):
    """
    Initialize the AgentMemoryManager with the given agent name and storage mode.

    Parameters:
    -----------
    agent_name : str
        The name of the agent.

    storage_mode : literal["mongodb", "json"], optional
        The storage mode to use, by default "mongodb".
    """
    self.agent_name = agent_name
    self.storage_mode = storage_mode

    if storage_mode == "mongodb":
      load_dotenv()
      self._client = MongoClient(os.getenv('MONGO_URI'))
      self._database = self._client[agent_name]
      self._memory_col = self._database[f'{agent_name}_memories']
      self._config_col = self._database[f'{agent_name}_config']

    elif storage_mode == "json":
      self.data_file = f"{agent_name}_data.json"
      default_structure = {
          'agent_name': agent_name,
          'status': "",
          'memories': []
      }

      if not os.path.exists(self.data_file):
        with open(self.data_file, 'w') as file:
          json.dump(default_structure, file,
                    default=self._datetime_serializer)

  def _datetime_serializer(self, obj):
    """
    Serializes datetime objects to ISO format.

    Parameters
    ----------
    obj : object
      The object to serialize.

    Returns
    -------
    str
      ISO formatted datetime string if obj is a datetime object.

    Raises
    ------
    TypeError
        If the object is not serializable.
    """
    if isinstance(obj, datetime.datetime):
      return obj.isoformat()
    raise TypeError("Type not serializable")

  def _datetime_deserializer(self, dct):
    """
    Deserializes datetime strings in a dictionary to datetime objects.

    Parameters
    ----------
    dct : dict
      The dictionary containing datetime strings.

    Returns
    -------
    dict
      The dictionary with datetime strings converted to datetime objects.
    """
    for key, value in dct.items():
      if key not in ['created_at', 'accessed_at']:
        continue
      try:
        dct[key] = dateutil.parser.parse(value)
      except (TypeError, ValueError):
        pass
    return dct

  def store_memory(self, memory: dict):
    """
    Stores a memory in the database or JSON file, depending on the storage mode.

    Parameters
    ----------
    memory : dict
      The memory to store.
    """
    if self.storage_mode == "mongodb":
      self._memory_col.insert_one(memory)
    elif self.storage_mode == "json":
      with open(self.data_file, 'r') as file:
        data = json.load(file, object_hook=self._datetime_deserializer)

      data['memories'].append(memory)

      with open(self.data_file, 'w') as file:
        json.dump(data, file, default=self._datetime_serializer)

  def retrieve_memory(self, description: str) -> dict | None:
    """
    Retrieves a memory based on its description.

    Parameters
    ----------
    description : str
      The description of the memory to retrieve.

    Returns
    -------
    dict or None
      The memory if found, otherwise None.
    """
    if self.storage_mode == "mongodb":
      return self._memory_col.find_one({'description': description})
    elif self.storage_mode == "json":
      with open(self.data_file, 'r') as file:
        data = json.load(file, object_hook=self._datetime_deserializer)

      for memory in data['memories']:
        if memory['description'] == description:
          return memory

      return None

  def retrieve_all_memories(self) -> list[dict]:
    """
    Retrieves all stored memories.

    Returns
    -------
    list of dict
      A list of all memories.
    """
    if self.storage_mode == "mongodb":
      return list(self._memory_col.find())
    elif self.storage_mode == "json":
      with open(self.data_file, 'r') as file:
        data = json.load(file, object_hook=self._datetime_deserializer)

      return data['memories']

  def get_agent_status(self) -> str | None:
    """
    Retrieves the current status of the agent.

    Returns
    -------
    str or None
      The current status of the agent, or None if not set.
    """
    if self.storage_mode == "mongodb":
      agent_data = self._config_col.find_one(
          {'agent_name': self.agent_name})
      return agent_data['status'] if agent_data else None
    elif self.storage_mode == "json":
      with open(self.data_file, 'r') as file:
        data = json.load(file, object_hook=self._datetime_deserializer)

      return data['status']

  def set_agent_status(self, status: str):
    """
    Sets the status of the agent.

    Parameters
    ----------
    status : str
      The new status to set for the agent.
    """
    if self.storage_mode == "mongodb":
      self._config_col.update_one({'agent_name': self.agent_name}, {'$set': {'status': status}}, upsert=True)
    elif self.storage_mode == "json":
      with open(self.data_file, 'r') as file:
        data = json.load(file, object_hook=self._datetime_deserializer)
      data['status'] = status

      with open(self.data_file, 'w') as file:
        json.dump(data, file, default=self._datetime_serializer)
