from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import SimpleDirectoryReader
from appconfig import appConfig

def load_documents(folder: str = '/'):
    loader = SimpleDirectoryReader(input_dir=appConfig.TRAINING_DATA_DIR + folder, required_exts=[".pdf", ".docx", ".txt"])
    all_docs = []
    for docs in loader.iter_data():
        all_docs.extend(docs)

    return all_docs

def create_vector_index(documents, embed_model, index_storage_name="index_store.json") -> VectorStoreIndex:
    print("Creating vector index...")
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
    )
    
    storage_context.persist(persist_dir=appConfig.VECTOR_STORAGE_DIR, index_store_fname=index_storage_name)
    return index
