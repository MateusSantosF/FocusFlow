import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
import nest_asyncio
from llama_index.agent.openai import OpenAIAgent
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from appconfig import appConfig

from agents.discipline_agent import get_discipline_tools
from agents.updates_agent import get_updates_tools

os.environ["OPENAI_API_KEY"] =  appConfig.OPENAI_API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]
Settings.chunk_size = 512
Settings.chunk_overlap = 64
Settings.llm = OpenAI(model="gpt-3.5-turbo")

# Aplicação FastAPI
app = FastAPI()

# Aplicar nest_asyncio para permitir operações assíncronas
nest_asyncio.apply()

# Modelo para a requisição do chat
class ChatRequest(BaseModel):
    message: str

tools = get_discipline_tools() +  get_updates_tools()
agent = OpenAIAgent.from_tools(tools, verbose=False)

@app.post("/chat")
async def chat(request: ChatRequest):
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")

    # Executar a resposta do agente de forma assíncrona
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, agent.chat, message)

    return {"response": str(response)}
