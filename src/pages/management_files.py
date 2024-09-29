import streamlit as st
from src.services.supabase_services import SUPABASE_CLIENT
from src.services.vector_index_services import recreate_vector_index

st.title("Arquivos de treinamento", anchor=False)
st.subheader("Arquivos atuais", anchor=False)
MAX_SIZE_IN_MB  = 500


def calculate_size_in_mb(file_list):
    total_size_in_kb  = sum(
        float(file.get("metadata", {}).get("size", 0))  # type: ignore
        for file in file_list
        if isinstance(file.get("metadata", {}).get("size", 0), (int, float)) # type: ignore
    )
    total_size_in_mb = total_size_in_kb / 10000
    return total_size_in_mb

st.cache_data(ttl=10)
def get_files():
    discipline_files = SUPABASE_CLIENT.storage.from_('disciplina').list()
    updates_files = SUPABASE_CLIENT.storage.from_('updates').list()
    total_size_in_mb = calculate_size_in_mb(discipline_files + updates_files)
    return discipline_files, updates_files, total_size_in_mb


discipline_files, updates_files, total_size_in_mb = get_files()
normalized_progress = min(total_size_in_mb / MAX_SIZE_IN_MB, 1)


if discipline_files or updates_files:
    if discipline_files:
        st.write("**Arquivos da Disciplina:**")
        for file in discipline_files:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(f"- {file['name']}")
            with col2:
                if st.button("Remover", key=f"del_discipline_{file['name']}"):
                    SUPABASE_CLIENT.storage.from_('disciplina').remove([file['name']])
                    st.success(f"Arquivo {file['name']} removido com sucesso!")
                    st.rerun()
    if updates_files:
        st.write("**Arquivos das Atualizações/Notas/Informações:**")
        for file in updates_files:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(f"- {file['name']}")
            with col2:
                if st.button("Remover", key=f"del_updates_{file['name']}"):
                    SUPABASE_CLIENT.storage.from_('updates').remove([file['name']])
                    st.success(f"Arquivo {file['name']} removido com sucesso!")
                    st.rerun()
    st.progress(normalized_progress, text=f"Total de espaço utilizado: {total_size_in_mb:.2f} MB de {MAX_SIZE_IN_MB} MB")
    
    if st.button("Treinar IA novamente", type="secondary", use_container_width=True):
        with st.spinner("Re-treinando IA..."):
            recreate_vector_index()
            st.session_state.chat_engine = None
            st.balloons()
            st.success("Treinamento realizado com sucesso!")
else:
    st.info("Nenhum arquivo encontrado.")

st.subheader("Adicionar novos arquivos")

uploaded_files = st.file_uploader(
    label="Selecione os arquivos para upload",
    accept_multiple_files=True,
    type=['pdf', 'docx', 'txt', 'pptx']
)

category = st.selectbox(
    "Selecione o tipo do(s) arquivo(s)",
    options=["Disciplina", "Atualizações"]
)

if st.button("Adicionar novos arquivos e treinar novamente", type="primary", use_container_width=True):
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_content = uploaded_file.read()
            file_name = uploaded_file.name
            category_bucket = 'disciplina' if category == "Disciplina" else 'updates'
            # Upload do arquivo para o SUPABASE_CLIENT Storage
            SUPABASE_CLIENT.storage.from_(category_bucket).upload(file_name, file_content, file_options={ "content-type": uploaded_file.type, "upsert": "true" })	
        
        with st.spinner("Re-treinando IA..."):
            st.session_state.chat_engine = None
            recreate_vector_index()
            st.success("IA treinada com sucesso!")
            st.balloons()
            uploaded_files= None
    else:
        st.warning("Nenhum arquivo selecionado para upload.")


