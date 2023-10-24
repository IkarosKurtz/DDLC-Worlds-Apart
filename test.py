from src.agent_memory.memory import Memory

data = {
  '_id': '111',
  'kind': 'aa',
  'description': 'aaaa',
  'retrieval_value': 'aaa',
  'importance': 'aaa',
  'references': 'aaa',
  'created_at': 'aaa',
  'accessed_at': 'aaa',
  'embedding': 'aaa'
}

memory = Memory(**data)

print(memory.id)