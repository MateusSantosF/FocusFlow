from llama_index.core.tools import QueryEngineTool, ToolMetadata, BaseTool
from open_ai_config import get_vector_index

def create_discipline_tools() -> list[BaseTool]:
    return [
        QueryEngineTool(
            query_engine=get_vector_index().as_query_engine(),
            metadata=ToolMetadata(
                name="discipline",
                description="Responde perguntas sobre a disciplina de Multimeios Didáticos"
            ),
        )
    ]

discipline_tools = create_discipline_tools()

def get_discipline_tools() -> list[BaseTool]:
    return discipline_tools
