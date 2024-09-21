import openai
from appconfig import appConfig
from agents.discipline_agent import get_discipline_tools
from agents.updates_agent import get_updates_tools
from llama_index.core import Settings
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer


def get_chat_agent()-> OpenAIAgent:
    openai.api_key = appConfig.OPENAI_API_KEY
    Settings.chunk_size = 512
    Settings.chunk_overlap = 64
    Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.6)
    memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
    sytem_prompt = """
    Você é um assistente virtual que pode responder perguntas sobre a  disciplina de Multimeios Didáticos e fornecer informações sobre atualizações, notas, provas, lembretes e informações da disciplina configuradas pelo professor. 
      
    ### Lembre-se: 
        - Responda com base no contexto fornecido
        - NUNCA fale sobre assuntos que não seja a disciplina; 
    """
    tools = get_discipline_tools() +  get_updates_tools()
    agent = OpenAIAgent.from_tools(tools, verbose=True, system_prompt=sytem_prompt, memory=memory)
    return agent

