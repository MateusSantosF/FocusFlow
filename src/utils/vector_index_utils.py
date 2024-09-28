import os
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import SimpleDirectoryReader
from src.configs.appconfig import appConfig
from llama_index.vector_stores.duckdb import DuckDBVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_index.core.node_parser import LangchainNodeParser
from src.utils.Constants import METADATA_AGENT_NAME_KEY
import shutil

def get_or_create_vector_index(force_create: bool = False) -> VectorStoreIndex:
    index_path = os.path.join(appConfig.VECTOR_STORAGE_DIR, "vector_store.duckdb")

    if os.path.exists(index_path) and not force_create:
        print("Carregando índice de vetores existente...")
        # Inicializa o DuckDBVectorStore com persistência
        vector_store = DuckDBVectorStore.from_local(index_path)
        index = VectorStoreIndex.from_vector_store(vector_store = vector_store)
        print("Índice de vetores carregado com sucesso.")
    else:
        print("Índice de vetores não encontrado. Criando um novo índice...")
        index = create_vector_index(force_create)
        print("Índice de vetores criado e armazenado com sucesso.")

    return index


def create_vector_index(force_create: bool = False) -> VectorStoreIndex:
    print("Creating vector index...")
    exists = os.path.exists(appConfig.VECTOR_STORAGE_DIR)

    if force_create and exists:
        print("Forçando a criação de um novo índice de vetores...")
        shutil.rmtree(appConfig.VECTOR_STORAGE_DIR)
        exists = False

    if not exists:
        os.makedirs(appConfig.VECTOR_STORAGE_DIR)
    
    # Carrega os documentos a partir do diretório de treinamento
    documents = SimpleDirectoryReader(
        input_dir=appConfig.TRAINING_DATA_DIR,
        required_exts=[".pdf", ".docx", ".txt"],
        recursive=True
    ).load_data()
    
    # printa o nome dos documetnos encontrados
    print("Documentos encontrados:")
    for doc in documents:
        print(doc.metadata["file_name"])
        file_path = doc.metadata["file_path"]
        relative_path = os.path.relpath(file_path, appConfig.TRAINING_DATA_DIR)
        agent_name = relative_path.split(os.sep)[0]
        doc.metadata[METADATA_AGENT_NAME_KEY] = agent_name

    parser = LangchainNodeParser(RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", "!", "?", ",", " "]
    ))


    token_nodes = parser.get_nodes_from_documents(
        documents, show_progress=True
    )
    # Inicializa o DuckDBVectorStore com persistência
    vector_store = DuckDBVectorStore(database_name=appConfig.DATABASE_FILE_NAME, persist_dir=appConfig.VECTOR_STORAGE_DIR)
    
    # Cria o contexto de armazenamento com o DuckDBVectorStore
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Cria o índice a partir dos documentos
    index = VectorStoreIndex(
        nodes=token_nodes,
        storage_context=storage_context,
        show_progress=True
    )
    
    # Persiste o índice no diretório especificado
    storage_context.persist(persist_dir=appConfig.VECTOR_STORAGE_DIR)
    print("Vector index created and stored.")
    return index
