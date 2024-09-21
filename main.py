import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import nest_asyncio
from llama_index.agent.openai import OpenAIAgent
from contextlib import asynccontextmanager
from open_ai_config import get_chat_agent


agent: OpenAIAgent
@asynccontextmanager
async def lifespan(_: FastAPI):
    global agent
    agent = get_chat_agent()
    yield

# Aplicação FastAPI
app = FastAPI(lifespan=lifespan)

# Aplicar nest_asyncio para permitir operações assíncronas
nest_asyncio.apply()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")

    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, agent.chat, message)

    return {"response": str(response)}
