from dotenv import load_dotenv
from pymongo import MongoClient
from typing import Literal as literal

import os
import json
import datetime
import dateutil.parser

class AgentMemoryManager:
  def __init__(self, agent_name: str, storage_mode: literal["mongodb", "json"] = "mongodb"):
    self.agent_name = agent_name
    self.storage_mode = storage_mode
        
    if storage_mode == "mongodb":
      load_dotenv()
      self.client = MongoClient(os.getenv('MONGO_URI'))
      self.database = self.client[agent_name]
      self.memory_col = self.database[f'{agent_name}_memories']
      self.config_col = self.database[f'{agent_name}_config']
            
    elif storage_mode == "json":
      self.data_file = f"{agent_name}_data.json"
      default_structure = {
        'agent_name': agent_name,
        'status': "",
        'memories': []
      }
            
      if not os.path.exists(self.data_file):
        with open(self.data_file, 'w') as file:
          json.dump(default_structure, file, default=self._datetime_serializer)
          
  def _datetime_serializer(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.isoformat()
    raise TypeError ("Type not serializable")
  
  def _datetime_deserializer(self, dct):
    for key, value in dct.items():
      if key not in ['created_at', 'accessed_at']: continue
      try:
        dct[key] = dateutil.parser.parse(value)
      except (TypeError, ValueError):
        pass
    return dct

  def store_memory(self, memory: dict):
    if self.storage_mode == "mongodb":
      self.memory_col.insert_one(memory)
    elif self.storage_mode == "json":
      with open(self.data_file, 'r') as file:
        data = json.load(file, object_hook=self._datetime_deserializer)
        
      data['memories'].append(memory)
            
      with open(self.data_file, 'w') as file:
        json.dump(data, file, default=self._datetime_serializer)

  def retrieve_memory(self, description: str) -> dict | None:
    if self.storage_mode == "mongodb":
      return self.memory_col.find_one({'description': description})
    elif self.storage_mode == "json":
      with open(self.data_file, 'r') as file:
        data = json.load(file, object_hook=self._datetime_deserializer)
        
      for memory in data['memories']:
        if memory['description'] == description:
          return memory
      
      return None

  def retrieve_all_memories(self) -> list[dict]:
    if self.storage_mode == "mongodb":
      return list(self.memory_col.find())
    elif self.storage_mode == "json":
      with open(self.data_file, 'r') as file:
        data = json.load(file, object_hook=self._datetime_deserializer)
        
      return data['memories']

  def get_agent_status(self) -> str | None:
    if self.storage_mode == "mongodb":
      agent_data = self.config_col.find_one({'agent_name': self.agent_name})
      return agent_data['status'] if agent_data else None
    elif self.storage_mode == "json":
      with open(self.data_file, 'r') as file:
        data = json.load(file, object_hook=self._datetime_deserializer)
        
      return data['status']

  def set_agent_status(self, status: str):
    if self.storage_mode == "mongodb":
      self.config_col.update_one({'agent_name': self.agent_name}, {'$set': {'status': status}}, upsert=True)
    elif self.storage_mode == "json":
      with open(self.data_file, 'r') as file:
        data = json.load(file, object_hook=self._datetime_deserializer)
      data['status'] = status
      
      with open(self.data_file, 'w') as file:
        json.dump(data, file, default=self._datetime_serializer)
