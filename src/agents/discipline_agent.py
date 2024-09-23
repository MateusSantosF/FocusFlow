from llama_index.core.tools import QueryEngineTool, ToolMetadata, BaseTool, RetrieverTool
from src.utils.vector_index_utils import get_or_create_vector_index

vector_index = get_or_create_vector_index()

def create_discipline_tools() -> list[BaseTool]:
    return [
        QueryEngineTool(
            query_engine=vector_index.as_query_engine(),
            metadata=ToolMetadata(
                name="discipline-agent",
                description="Responde perguntas sobre a disciplina de Multimeios Didáticos"
            ),
        )
    ]

discipline_tools = create_discipline_tools()

def get_discipline_tools() -> list[BaseTool]:
    return discipline_tools
