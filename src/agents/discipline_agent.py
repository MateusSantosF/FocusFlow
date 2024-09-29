from llama_index.core.tools import QueryEngineTool, ToolMetadata, BaseTool, RetrieverTool
from src.utils.Constants import DISCIPLINE_AGENT_NAME, METADATA_AGENT_NAME_KEY
from src.services.vector_index_services import get_vector_index
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
from llama_index.core.vector_stores.types import VectorStoreQueryMode


def create_discipline_tools() -> list[BaseTool]:
    vector_index = get_vector_index()
    
    filters = MetadataFilters(
        filters=[ExactMatchFilter(key=METADATA_AGENT_NAME_KEY, value=DISCIPLINE_AGENT_NAME)]
    )
    return [
        RetrieverTool(
            retriever=vector_index.as_retriever(similarity_top_k=10, filters=filters,vector_store_query_mode= VectorStoreQueryMode.TEXT_SEARCH),
            metadata=ToolMetadata(
                name=DISCIPLINE_AGENT_NAME,
                description="Responde perguntas sobre a disciplina de Multimeios Didáticos"
            ),
        )
    ]

def get_discipline_tools() -> list[BaseTool]:
    return create_discipline_tools()
