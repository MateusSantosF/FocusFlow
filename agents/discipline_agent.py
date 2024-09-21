from llama_index.core.tools import QueryEngineTool, ToolMetadata, BaseTool
from local_embedding_model import LocalBertEmbedding
from vector_index_utils import create_vector_index, load_documents


embeddings = LocalBertEmbedding(model_name='neuralmind/bert-base-portuguese-cased')
documents = load_documents(folder='/disciplina')
vector_index = create_vector_index(documents=documents, embed_model=embeddings,index_storage_name="discipline_index_store.json")

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
