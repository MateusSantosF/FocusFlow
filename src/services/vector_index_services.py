from pathlib import Path
from typing import List
from llama_index.core import VectorStoreIndex, StorageContext
from src.configs.appconfig import appConfig
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_index.core.node_parser import LangchainNodeParser
from src.services.supabase_services import SUPABASE_CLIENT
from src.utils.Constants import METADATA_AGENT_NAME_KEY
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.supabase import SupabaseVectorStore
from llama_index.core import Document
from llama_index.readers.file import PDFReader,DocxReader, FlatReader
import tempfile
import os

def get_vector_index() -> VectorStoreIndex:
    vector_store = SupabaseVectorStore(
        postgres_connection_string=appConfig.DATABASE_URL,
        dimension=1536, 
        collection_name=appConfig.SUPABASE_VECTORS_COLLECTION,
    )
    index = VectorStoreIndex.from_vector_store(vector_store = vector_store)
    return index


def recreate_vector_index() -> VectorStoreIndex:
    print("re-creating vector index...")
    SUPABASE_CLIENT.postgrest.from_table('embeddings').delete()
    # Lista arquivos dos buckets no Supabase
    discipline_files = SUPABASE_CLIENT.storage.from_('disciplina').list()
    updates_files = SUPABASE_CLIENT.storage.from_('updates').list()
    
    # Lista para armazenar os documentos convertidos
    all_files = discipline_files + updates_files
    documents: List[Document] = []

    # List to keep track of temporary files for cleanup
    temp_files = []

    # Função auxiliar para converter o arquivo em documento
    def file_to_document(file_name, file_content, mimetype)-> List[Document]:
        print(f"Processing file: {file_name} - {mimetype}")
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, prefix=file_name + "-") as tmp_file:
            tmp_file.write(file_content)
            tmp_file.flush()
            file_path = tmp_file.name
            temp_files.append(file_path)  # Keep track of temp files to delete later

        # Choose the appropriate loader based on the mimetype
        if mimetype == "pdf":
            loader = PDFReader()
        elif mimetype == "docx":
            loader = DocxReader()
        elif mimetype == "txt":
            loader = FlatReader()
        else:
            print(f"Unsupported file type: {file_name} {mimetype}")
            return []
  

        return loader.load_data(file=Path(file_path))

    # Faz o download de cada arquivo e converte para documento
    for file_info in all_files:
        print(file_info)
        file_name = file_info['name']
        mimetype = file_name.split('.')[-1]
        # Download do arquivo do Supabase
        bucket_name = 'disciplina' if file_info in discipline_files else 'updates'
        file_content = SUPABASE_CLIENT.storage.from_(bucket_name).download(file_name)  # Ajustar conforme o bucket correto
        doc = file_to_document(file_name, file_content, mimetype)[0]
        doc.metadata[METADATA_AGENT_NAME_KEY] = bucket_name
        doc.metadata["file_path"] = None
        documents.append(doc)  # Adiciona o documento à lista

    # Combina documentos locais e os carregados do Supabase

    # Printando o nome dos documentos encontrados
    print("Documentos encontrados:")
    for doc in documents:
        doc.metadata
        print(doc.metadata.get("file_name", "Unknown File"))

    # Parse e processamento dos documentos como na lógica anterior
    parser = LangchainNodeParser(RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", "!", "?", ",", " "]
    ))

    token_nodes = parser.get_nodes_from_documents(documents, show_progress=True)

    vector_store = SupabaseVectorStore(
        postgres_connection_string=appConfig.DATABASE_URL,
        dimension=1536,
        collection_name="embeddings",
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex(
        nodes=token_nodes,
        storage_context=storage_context,
        show_progress=True
    )

    # Clean up temporary files
    for file_path in temp_files:
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Error deleting temporary file {file_path}: {e}")

    print("Vector index created and stored.")
    return index