from llama_index.core.tools import QueryEngineTool, ToolMetadata, BaseTool, RetrieverTool
from src.utils.vector_index_utils import get_or_create_vector_index


def create_discipline_tools() -> list[BaseTool]:
    vector_index = get_or_create_vector_index()

    return [
        QueryEngineTool(
            query_engine=vector_index.as_query_engine(),
            metadata=ToolMetadata(
                name="discipline-agent",
                description="Responde perguntas sobre a disciplina de Multimeios Didáticos"
            ),
        )
    ]

def get_discipline_tools() -> list[BaseTool]:
    return create_discipline_tools()
