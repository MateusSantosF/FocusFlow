from llama_index.core import VectorStoreIndex, StorageContext
from src.configs.appconfig import appConfig
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_index.core.node_parser import LangchainNodeParser
from src.services.supabase_services import SUPABASE_CLIENT
from src.utils.Constants import METADATA_AGENT_NAME_KEY
from llama_index.vector_stores.supabase import SupabaseVectorStore
from llama_index.core import SimpleDirectoryReader

import tempfile
import os
import shutil

def get_vector_index() -> VectorStoreIndex:
    vector_store = SupabaseVectorStore(
        postgres_connection_string=appConfig.DATABASE_URL,
        dimension=1536, 
        collection_name=appConfig.SUPABASE_VECTORS_COLLECTION,
    )
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    return index


def recreate_vector_index() -> VectorStoreIndex:
    print("Recriando o índice vetorial...")

    # Cria um diretório temporário para armazenar os arquivos
    temp_dir = tempfile.mkdtemp(prefix="focus_flow_temp_files_")
    print(f"Diretório temporário criado em: {temp_dir}")

    try:
        # Lista os arquivos nos buckets 'disciplina' e 'updates'
        discipline_files = SUPABASE_CLIENT.storage.from_('disciplina').list()
        updates_files = SUPABASE_CLIENT.storage.from_('updates').list()
        
        all_files = discipline_files + updates_files

        # Função para baixar arquivos do Supabase para o diretório temporário
        def download_file_to_temp(file_info, bucket_name):
            file_name = file_info['name']
            print(f"Baixando arquivo: {file_name} do bucket: {bucket_name}")
            file_content = SUPABASE_CLIENT.storage.from_(bucket_name).download(file_name)
            file_path = os.path.join(temp_dir, file_name)
            
            # Garante que o diretório existe
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'wb') as f:
                f.write(file_content)
            # Opcional: Definir metadados como parte do nome ou através de arquivos auxiliares
            return file_path

        # Baixa todos os arquivos para o diretório temporário
        for file_info in all_files:
            bucket_name = 'disciplina' if file_info in discipline_files else 'updates'
            download_file_to_temp(file_info, bucket_name)

        print("Todos os arquivos foram baixados para o diretório temporário.")

        reader = SimpleDirectoryReader(
            input_dir=temp_dir,
            recursive=False,
            filename_as_id=True,
        )
        documents = reader.load_data(show_progress=True)

        # Opcional: Adicionar metadados adicionais aos documentos
        for doc in documents:
            # Aqui, você pode extrair o bucket a partir do caminho do arquivo ou outra lógica
            # Exemplo simplificado:
            file_name = os.path.basename(doc.metadata.get("file_path", ""))
            if file_name in [f['name'] for f in discipline_files]:
                bucket = 'disciplina'
            else:
                bucket = 'updates'
            doc.metadata[METADATA_AGENT_NAME_KEY] = bucket
            doc.metadata["file_path"] = None  # Remova ou ajuste conforme necessário

        print("Documentos carregados pelo SimpleDirectoryReader.")

        # Configura o parser e divide os textos
        parser = LangchainNodeParser(RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=64,
            separators=["\n\n", "\n"]
        ))

        token_nodes = parser.get_nodes_from_documents(documents, show_progress=True)

        # Configura o armazenamento vetorial
        vector_store = SupabaseVectorStore(
            postgres_connection_string=appConfig.DATABASE_URL,
            dimension=1536,
            collection_name="embeddings",
        )

        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Cria o índice vetorial
        index = VectorStoreIndex(
            nodes=token_nodes,
            storage_context=storage_context,
            show_progress=True
        )

        print("Índice vetorial criado e armazenado.")
        return index

    finally:
        # Garante que o diretório temporário seja removido
        try:
            shutil.rmtree(temp_dir)
            print(f"Diretório temporário {temp_dir} removido com sucesso.")
        except Exception as e:
            print(f"Erro ao remover o diretório temporário {temp_dir}: {e}")
