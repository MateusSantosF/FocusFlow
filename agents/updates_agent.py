from llama_index.core.tools import QueryEngineTool, ToolMetadata, BaseTool
from local_embedding_model import LocalBertEmbedding
from vector_index_utils import create_vector_index, load_documents


embeddings = LocalBertEmbedding(model_name='neuralmind/bert-base-portuguese-cased')
documents = load_documents(folder='/updates')
vector_index = create_vector_index(documents=documents, embed_model=embeddings,index_storage_name="update_index_store.json")

def create_updates_tools() -> list[BaseTool]:
    return [
        QueryEngineTool(
            query_engine=vector_index.as_query_engine(),
            metadata=ToolMetadata(
                name="updates-agent",
                description="Responde sobre atualizações, notas, provas, lembretes e informações da disciplina configuradas pelo professor."
            ),
        )
    ]

updates_tools = create_updates_tools()

def get_updates_tools()-> list[BaseTool]:
    return updates_tools
