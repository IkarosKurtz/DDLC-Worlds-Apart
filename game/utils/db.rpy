init -999 python:
  from typing import Literal as literal

  import os
  import json
  import datetime
  import time
  import dateutil.parser


  class JSONDatabase:
    """ A class to manage an agent's data like memories, status, bio and name."""

    def __init__(self, agent_name: str):
      """
      Used to store and retrieve memories and status for an agent.
      Parameters:
      -----------
      agent_name : str
          The name of the agent.
      """
      self.agent_name = agent_name
      self.data_folder = os.path.join(renpy.config.gamedir, "agents_data")

      structure = {
          'agent_name': agent_name,
          'status': "",
          'bio': "",
          'location': "",
          'memories': []
      }

      if not os.path.exists(self.data_folder):
        os.mkdir(self.data_folder)

      agent_folder = os.path.join(self.data_folder, f"{agent_name}")

      if not os.path.exists(agent_folder):
        os.mkdir(agent_folder)

      self.data_file = os.path.join(agent_folder, f"{agent_name}_memories.json")

      if not os.path.exists(self.data_file):
        with open(self.data_file, 'w', encoding='utf-8') as file:
          json.dump(structure, file,indent=2)

    def _datetime_serializer(self, obj):
      """
      Serializes datetime objects to ISO format.

      Deperecated
      -----------
        datetiem objects where replaced by a timestamp

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

      Deperecated
      -----------
        datetiem objects where replaced by a timestamp

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
      Stores a memory in the JSON file.

      Parameters
      ----------
      memory : dict
        The memory to store.
      """
      with open(self.data_file, 'r', encoding='utf-8') as file:
        time.sleep(.06)
        data = json.load(file)

      data['memories'].append(memory)

      with open(self.data_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

    def store_memories(self, memories: list[dict]):
      """
      Stores a list of memories in the JSON file.

      Parameters
      ----------
      memories : list[dict]
        The list of memories to store.
      """
      with open(self.data_file, 'r', encoding='utf-8') as file:
        time.sleep(.06)
        data = json.load(file)

      data['memories'].extend(memories)

      with open(self.data_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

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
      with open(self.data_file, 'r', encoding='utf-8') as file:
        time.sleep(.06)
        data = json.load(file)

      if any(memory['description'] == description for memory in data['memories']):
        return next((memory for memory in data['memories'] if memory['description'] == description), None)

    def retrieve_all_memories(self) -> list[dict]:
      """
      Retrieves all stored memories.

      Returns
      -------
      list of dict
        A list of all memories.
      """
      with open(self.data_file, 'r', encoding='utf-8') as file:
        time.sleep(.06)
        data = json.load(file)

      return data['memories'] if 'memories' in data else []

    def get_agent_status(self) -> str:
      """
      Retrieves the current status of the agent.

      Returns
      -------
      str
        The current status of the agent.
      """
      with open(self.data_file, 'r', encoding='utf-8') as file:
        time.sleep(.06)
        data = json.load(file)

      return data['status'] if 'status' in data else None

    def set_agent_status(self, status: str):
      """
      Sets the status of the agent.

      Parameters
      ----------
      status : str
        The new status to set for the agent.
      """
      with open(self.data_file, 'r', encoding='utf-8') as file:
        time.sleep(.06)
        data = json.load(file)
      data['status'] = status

      with open(self.data_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

    def get_agent_bio(self) -> str:
      """
      Retrieves the biography of the agent.

      Returns
      -------
      str
        The biography of the agent.
      """
      with open(self.data_file, 'r', encoding='utf-8') as file:
        time.sleep(.06)
        data = json.load(file)

      return data['bio'] if 'bio' in data else None

    def set_agent_bio(self, bio: str):
      """
      Sets the biography of the agent.

      Parameters
      ----------
      bio : str
        The new biography of the agent.
      """
      with open(self.data_file, 'r', encoding='utf-8') as file:
        time.sleep(.06)
        data = json.load(file)
      data['bio'] = bio

      with open(self.data_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

    def get_agent_location(self) -> str:
      """
      Retrieves the current location of the agent.

      Returns
      -------
      str
        The current location of the agent.
      """
      with open(self.data_file, 'r', encoding='utf-8') as file:
        time.sleep(.06)
        data = json.load(file)

      return data['location'] if 'location' in data else None

    def set_agent_location(self, location: str):
      """
      Sets the location of the agent.

      Parameters
      ----------
      location : str
        The new location of the agent.
      """
      with open(self.data_file, 'r', encoding='utf-8') as file:
        time.sleep(.06)
        data = json.load(file)
      data['location'] = location

      with open(self.data_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)