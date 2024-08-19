init -999 python:
  import requests
  import math
  import random

  headers = headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
  }

   
  def chat_completion(prompt: str, ai_role: str = 'You are a helpful assistant.', temperature: float = 0) -> tuple[str, str]:
    response = requests.post(
      "http://localhost:11434/v1/chat/completions",
      headers={
        "Content-Type": "application/json"
      },
      json={
        "model": "llama3",
        "stream": False,
        "seed": persistent.seed,
        "temperature": temperature,
        "messages": [
          {
            "role": "system",
            "content": ai_role
          },
          {
            "role": "user",
            "content": prompt
          }
        ]
      }
    ).json()

    message = response['choices'][0]['message']['content']
    tokens = response['usage']['total_tokens']

    return (message, tokens)


  def get_embedding(text: str, engine: str = 'text-embedding-ada-002') -> list[float]:
    data = {
      "input": text,
      "model": engine,
      "encoding_format": "float"
    }

    response = requests.post(
      "http://localhost:11434/api/embeddings",
      json={
        "model": "all-minilm",
        "prompt": text
      }
    )
    
    if response.status_code != 200:
      raise Exception(response.text)
    
    response = response.json()
    
    embedding = response['embedding']
    return embedding

  def dot_product(vector1, vector2):
    return sum(v1 * v2 for v1, v2 in zip(vector1, vector2))

  def magnitude(vector):
    return math.sqrt(sum(v ** 2 for v in vector))

  def cosine_similarity(embedding1, embedding2):
    dot_prod = dot_product(embedding1, embedding2)
    magnitude1 = magnitude(embedding1)
    magnitude2 = magnitude(embedding2)
    if magnitude1 == 0 or magnitude2 == 0:
      return 0.0
    
    return dot_prod / (magnitude1 * magnitude2)