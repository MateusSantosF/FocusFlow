from llama_index.core.tools import QueryEngineTool, ToolMetadata, BaseTool, RetrieverTool
from src.utils.vector_index_utils import  get_or_create_vector_index

vector_index = get_or_create_vector_index()

def create_updates_tools() -> list[BaseTool]:
    return [
        QueryEngineTool(
            query_engine=vector_index.as_query_engine(),
            metadata=ToolMetadata(
                name="updates-agent",
                description="Responde sobre atualizações, notas, provas, lembretes e informações da disciplina configuradas pelo professor."
            ),
        ),
       
    ]

updates_tools = create_updates_tools()

def get_updates_tools()-> list[BaseTool]:
    return updates_tools
