import os
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import SimpleDirectoryReader
from src.configs.appconfig import appConfig
from src.configs.local_embedding_model import LocalBertEmbedding
from llama_index.core import load_index_from_storage

def get_or_create_vector_index():
    index_path = os.path.join(appConfig.VECTOR_STORAGE_DIR)

    if os.path.exists(index_path) and any(os.scandir(index_path)):
        print("Carregando índice de vetores existente...")
        storage_context = StorageContext.from_defaults(persist_dir=appConfig.VECTOR_STORAGE_DIR)
        index = load_index_from_storage(storage_context)
        print("Índice de vetores carregado com sucesso.")
    else:
        print("Índice de vetores não encontrado. Criando um novo índice...")
        index = create_vector_index()
    print("Índice de vetores criado e armazenado com sucesso.")

    return index



def create_vector_index() -> VectorStoreIndex:
    print("Creating vector index...")
    exists = os.path.exists(appConfig.VECTOR_STORAGE_DIR)
    if not exists:
        os.makedirs(appConfig.VECTOR_STORAGE_DIR)
    documents  = SimpleDirectoryReader(input_dir=appConfig.TRAINING_DATA_DIR, required_exts=[".pdf", ".docx", ".txt"], recursive=True).load_data()
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )
    storage_context.persist(persist_dir=appConfig.VECTOR_STORAGE_DIR)
    print("Vector index created and stored.")
    return index
