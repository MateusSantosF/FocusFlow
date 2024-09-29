from llama_index.core.tools import ToolMetadata, BaseTool, RetrieverTool
from src.utils.Constants import METADATA_AGENT_NAME_KEY, UPDATE_AGENT_NAME
from src.services.vector_index_services import  get_vector_index
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
from llama_index.core.vector_stores.types import VectorStoreQueryMode


def create_updates_tools() -> list[BaseTool]:
    vector_index = get_vector_index()

    filters = MetadataFilters(
        filters=[ExactMatchFilter(key=METADATA_AGENT_NAME_KEY, value=UPDATE_AGENT_NAME)]
    )

    return [
        RetrieverTool(
            retriever=vector_index.as_retriever(similarity_top_k=3, filters=filters,vector_store_query_mode= VectorStoreQueryMode.TEXT_SEARCH),
            metadata=ToolMetadata(
                name=UPDATE_AGENT_NAME,
                description="Responde sobre atualizações, notas, provas, lembretes e informações da disciplina."
            ),
        ),
       
    ]

def get_updates_tools()-> list[BaseTool]:
    return create_updates_tools()
