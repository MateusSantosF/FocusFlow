from llama_index.core.tools import QueryEngineTool, ToolMetadata, BaseTool
from open_ai_config import get_vector_index

def create_updates_tools() -> list[BaseTool]:
    return [
        QueryEngineTool(
            query_engine=get_vector_index().as_query_engine(),
            metadata=ToolMetadata(
                name="updates",
                description="Responde sobre atualizações, notas, provas, lembretes e informações da disciplina configuradas pelo professor."
            ),
        )
    ]

updates_tools = create_updates_tools()

def get_updates_tools()-> list[BaseTool]:
    return updates_tools
