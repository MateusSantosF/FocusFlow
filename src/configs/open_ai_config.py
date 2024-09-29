from src.agents.discipline_agent import get_discipline_tools
from src.agents.updates_agent import get_updates_tools
from llama_index.core import Settings
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
from src.configs.appconfig import appConfig
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType, OpenAIEmbeddingMode


def build_chat_engine()->OpenAIAgent:
    Settings.chunk_size = 512
    Settings.chunk_overlap = 128
    Settings.num_output = 700 # number of tokens reserved for text generation.
    Settings.context_window = 4096 # maximum input size to the LLM
    Settings.embed_model = OpenAIEmbedding(model=OpenAIEmbeddingModelType.TEXT_EMBED_3_SMALL, api_key=appConfig.OPENAI_API_KEY, max_retries= 4)
    Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.6, api_key=appConfig.OPENAI_API_KEY)
    memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
    sytem_prompt = """
    Você é um assistente virtual que pode responder perguntas sobre a  disciplina de Multimeios Didáticos e fornecer informações sobre atualizações, notas, provas, lembretes e informações da disciplina configuradas pelo professor. 
      
    ### Lembre-se: 
        - Responda APENAS com base no contexto fornecido
        - NUNCA fale sobre assuntos que não seja a disciplina; 
    """
    tools = get_discipline_tools() +  get_updates_tools()
    agent = OpenAIAgent.from_tools(tools, verbose=True, system_prompt=sytem_prompt, memory=memory)
    return agent

