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
  
  response, pose = agent.chat(speaker, message)
  
  print(f'{pose}: {response}')

  return {
    "response": response,
    "character": agent.character_data.name,
    "pose": pose
  }
  
if __name__ == '__main__':
  import uvicorn
  uvicorn.run(app, host='localhost', port=8080)