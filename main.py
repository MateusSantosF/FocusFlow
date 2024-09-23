import streamlit as st


# Definição das páginas
LOGIN_PAGE = st.Page("src/pages/login.py", title="Login")
CHAT_PAGE = st.Page("src/pages/chat.py", title="💬 Chat", default=True)
SETTINGS_PAGE = st.Page("src/pages/settings.py", title="⚙️ Configurações")

# Configuração da página
st.set_page_config(page_title="Tutor Virtual - IFSP SJBV", layout="centered")
# Inicializar o estado da sessão
if 'authenticated_role' not in st.session_state.keys():
    st.session_state.authenticated_role = None
    
# Função para reiniciar a aplicação
def reset_session():
    st.session_state.authenticated_role = None
    st.session_state.authentication_status = None
    st.session_state.name = None
    st.session_state.username = None
    st.session_state.sidebar = 'collapsed'
    print("Sessão reiniciada.")
    st.rerun()

if st.session_state.authenticated_role is None:
    st.navigation([LOGIN_PAGE])
    LOGIN_PAGE.run()

if st.session_state.authenticated_role is not None:
    role = st.session_state.authenticated_role
    if st.sidebar.button("Deslogar", type='secondary', use_container_width=True):
            reset_session()

    pg = st.navigation([CHAT_PAGE, SETTINGS_PAGE])
    pg.run()