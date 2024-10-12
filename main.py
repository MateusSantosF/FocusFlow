import streamlit as st

from src.configs.logger import setup_logging
import sys

from src.configs.open_ai_config import build_chat_engine
sys.dont_write_bytecode = True

# Definição das páginas
LOGIN_PAGE = st.Page("src/pages/login.py", title="Login")
CHAT_PAGE = st.Page("src/pages/chat.py", title="💬 Chat", default=True)
SETTINGS_PAGE = st.Page("src/pages/settings.py", title="⚙️ Configurações")
FILES_MANAGEMENT_PAGE = st.Page("src/pages/management_files.py", title="🗃️ Arquivos de Treinamento")


# Configuração da página
st.set_page_config(page_title="Tutor Virtual - IFSP SJBV", layout="centered")
# Inicializar o estado da sessão
if 'authenticated_role' not in st.session_state.keys():
    st.session_state.authenticated_role = None

if "chat_engine" not in st.session_state or st.session_state.chat_engine is None:
    setup_logging()
    st.session_state.chat_engine = build_chat_engine()


# Função para reiniciar a aplicação
def reset_session():
    st.session_state.authenticated_role = None
    st.session_state.authentication_status = None
    st.session_state.name = None
    st.session_state.username = None
    st.session_state.sidebar = 'collapsed'
    st.rerun()

if st.session_state.authenticated_role is None:
    st.navigation([LOGIN_PAGE])
    LOGIN_PAGE.run()

if st.session_state.authenticated_role is not None:
    role = st.session_state.authenticated_role
    if st.sidebar.button("Deslogar", type='secondary', use_container_width=True):
            reset_session()

    if role == "admin":
        pg = st.navigation([CHAT_PAGE, SETTINGS_PAGE, FILES_MANAGEMENT_PAGE])
    else:
        pg = st.navigation([CHAT_PAGE, SETTINGS_PAGE])
    pg.run()