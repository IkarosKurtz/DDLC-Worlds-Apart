from openai.error import ServiceUnavailableError
import openai

def chat_completion(prompt: str, ai_role: str = 'You are a helpful assistant.', ) -> tuple[str]:
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
