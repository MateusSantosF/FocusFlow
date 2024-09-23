from llama_index.core.tools import QueryEngineTool, ToolMetadata, BaseTool, RetrieverTool
from src.utils.vector_index_utils import  get_or_create_vector_index


def create_updates_tools() -> list[BaseTool]:
    vector_index = get_or_create_vector_index()

    return [
        QueryEngineTool(
            query_engine=vector_index.as_query_engine(),
            metadata=ToolMetadata(
                name="updates-agent",
                description="Responde sobre atualizações, notas, provas, lembretes e informações da disciplina configuradas pelo professor."
            ),
        ),
       
    ]

def get_updates_tools()-> list[BaseTool]:
    return create_updates_tools()
