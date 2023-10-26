from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main import agent

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.get("/chat")
def chat(message, speaker):
  print(message, speaker)
  
  list_of_responses = agent.chat(speaker, message)
  
  for [pose, response] in list_of_responses:
    print(f'{pose}: {response}')

  return {
    "character": agent.character_data.name,
    "responses": list_of_responses
  }
  
if __name__ == '__main__':
  import uvicorn
  uvicorn.run(app, host='localhost', port=8080)