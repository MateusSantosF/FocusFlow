from llama_index.core import VectorStoreIndex, StorageContext
from appconfig import appConfig
from local_embedding_model import LocalBertEmbedding
from llama_index.core import SimpleDirectoryReader

def load_documents():
    loader = SimpleDirectoryReader(input_dir=appConfig.TRAINING_DATA_DIR, required_exts=[".pdf", ".docx", ".txt"])
    all_docs = []
    for docs in loader.iter_data():
        all_docs.extend(docs)

    return all_docs

def create_vector_index(documents, embed_model):
    print("Creating vector index...")
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model
    )
    
    storage_context.persist(persist_dir=appConfig.VECTOR_STORAGE_DIR)
    return index

embeddings = LocalBertEmbedding(model_name='neuralmind/bert-base-portuguese-cased')
documents = load_documents()
vector_index = create_vector_index(documents=documents, embed_model=embeddings)

def get_vector_index() -> VectorStoreIndex:
    return vector_index
