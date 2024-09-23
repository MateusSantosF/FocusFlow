import streamlit as st
from src.utils.auth import criar_autenticador, carregar_config  

authenticator = criar_autenticador()
config = carregar_config()

st.title("Bem-vindo ao Tutor Virtual", anchor=False)
CHAT_PAGE = st.Page("src/pages/chat.py", title="💬 Chat", default=True)

role = st.radio("Como deseja entrar?", ("Aluno", "Professor"))
current_access_code = config.get('acesso_aluno')

if role == "Aluno":
    st.subheader("Entrar como Aluno")
    with st.form(key="form_login_aluno"):
        codigo = st.text_input("Digite o código de acesso:", type="default")
        if st.form_submit_button("Entrar como Aluno", type="primary"):
            if codigo == current_access_code:
                st.session_state['authentication_status'] = True
                st.session_state.authenticated_role = "Aluno"
                st.toast("Autenticação bem-sucedida!")
                st.switch_page(CHAT_PAGE)
            else:
                st.error("Código de acesso inválido.")

else:
    st.subheader("Entrar como professor")
    name, authentication_status, username = authenticator.login(key='Login', location='main')

    if authentication_status:
        if username == 'admin':
            st.session_state.authenticated_role = "admin"
            st.session_state['authentication_status'] = authentication_status
            st.session_state['name'] = name
            st.session_state['username'] = username
            st.rerun()
        else:
            st.error("Acesso restrito apenas para professores.")
    else:
        if authentication_status == False:
            st.error('Usuário ou senha incorretos')
        elif authentication_status == None:
            st.warning('Por favor, insira seu usuário e senha')