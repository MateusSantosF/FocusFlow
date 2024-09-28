import streamlit as st
import os
from pathlib import Path

from src.configs.appconfig import appConfig
from src.utils.vector_index_utils import get_or_create_vector_index

def list_training_files():

    st.subheader("Arquivos atuais", anchor=False)
    training_dir = Path(appConfig.TRAINING_DATA_DIR)
    if not training_dir.exists():
        os.makedirs(training_dir)
        os.makedirs(training_dir / "disciplina")
        os.makedirs(training_dir / "updates")

    discipline_files = []
    updates_files = []

    for root, dirs, files in os.walk(training_dir):
        for file in files:
            file_path = Path(root) / file
            # Determine the category based on the parent directory
            relative_path = file_path.relative_to(training_dir)
            category = relative_path.parts[0] if len(relative_path.parts) > 1 else "Uncategorized"
            if category == "disciplina":
                discipline_files.append(file_path)
            elif category == "updates":
                updates_files.append(file_path)

    if discipline_files or updates_files:
        if discipline_files:
            st.write("**Arquivos da Disciplina:**")
            for file_path in discipline_files:
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    st.write(f"- {file_path.name}")
                with col2:
                    if st.button("Remover", key=f"del_discipline_{file_path.name}"):
                        os.remove(file_path)
                        st.success(f"Arquivo {file_path.name} removido com sucesso!")
                        st.rerun()
        if updates_files:
            st.write("**Arquivos das Atualizações/Notas/Informações:**")
            for file_path in updates_files:
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    st.write(f"- {file_path.name}")
                with col2:
                    if st.button("Remover", key=f"del_updates_{file_path.name}"):
                        os.remove(file_path)
                        st.success(f"Arquivo {file_path.name} removido com sucesso!")
    
        if st.button("Treinar IA novamente", type="secondary", use_container_width=True):
            with st.spinner("Re-treinando IA..."):
                        get_or_create_vector_index(force_create=True)
                        st.session_state.chat_engine = None
                        st.success("Arquivos enviados com sucesso!")
                        st.rerun()                  
    else:
        st.info("Nenhum arquivo encontrado.")

def upload_training_files():
    st.subheader("Adicionar novos arquivos")

    uploaded_files = st.file_uploader(
        label="Selecione os arquivos para upload",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt']
    )

    category = st.selectbox(
        "Selecione o tipo do(s) arquivo(s)",
        options=["Disciplina", "Atualizações"]
    )

    if st.button("Adicionar novos arquivos e treinar novamente", type="primary", use_container_width=True):
        if uploaded_files:
            for uploaded_file in uploaded_files:
                category_dir = "disciplina" if category == "Disciplina" else "updates"
                save_path = Path(appConfig.TRAINING_DATA_DIR) / category_dir / uploaded_file.name
                save_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
            
            with st.spinner("Re-treinando IA..."):
                get_or_create_vector_index(force_create=True)
                st.session_state.chat_engine = None
                st.success("Arquivos enviados com sucesso!")
                st.rerun()
        else:
            st.warning("Nenhum arquivo selecionado para upload.")

st.title("Arquivos de treinamento", anchor=False)

list_training_files()
upload_training_files()
