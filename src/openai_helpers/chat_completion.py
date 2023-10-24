import os
from dotenv import load_dotenv
import openai
from openai.error import ServiceUnavailableError
import time
load_dotenv()

openai.api_key = os.getenv('OPENAI')

def chat_completion(ai_role: str, prompt: str) -> tuple[str]:
  response = None

  while response == None:
    try:
      response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
          {'role': 'system', 'content': ai_role},
          {'role': 'user', 'content': prompt},
        ]
      )
    except ServiceUnavailableError as e:
      message = e._message
      if message != 'The server is overloaded or not ready yet.':
        raise e
      
      continue
  
  message = response.choices[0].message.content
  tokens = response['usage']['total_tokens']

  return (message, tokens)
