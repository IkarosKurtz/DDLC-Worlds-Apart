from src.character import Character
from dotenv import load_dotenv
from data import monika

import os
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

agent = Character('Monika', monika['bio'], monika['habilites'], monika['memories'], monika['traits'])

if __name__ == '__main__':
  while True:
    user_input = input('> ')
    print(agent.chat('Ikaros', user_input))