import streamlit as st

from src.services.supabase_services import SUPABASE_CLIENT

st.title("Bem-vindo ao Tutor Virtual", anchor=False)
CHAT_PAGE = st.Page("src/pages/chat.py", title="💬 Chat", default=True)

role = st.radio("Como deseja entrar?", ("Aluno", "Professor"))
current_access_code = "SJBV2024"

st.cache_resource(ttl=60)
def get_current_config():
    result = SUPABASE_CLIENT.schema("public").table("access_configs").select("*").execute()
    config = result.data[0]
    current_access_code = config['access_code']
    admin_email = config['admin_email']
    admin_password = config['admin_password']

    return current_access_code, admin_email, admin_password

current_access_code, admin_email, admin_password = get_current_config()


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
    with st.form(key="form_login_aluno"):
        email = st.text_input("E-mail", type="default")
        password = st.text_input("Senha", type="password")

        if st.form_submit_button("Entrar como Professor", type="primary"):
            if email == "" or password == "":
                st.error("Por favor, preencha todos os campos.")
            elif email == admin_email and password == admin_password:
                st.session_state['authentication_status'] = True
                st.session_state.authenticated_role = "admin"
                st.session_state['name'] = "Admin"
                st.session_state['username'] = "admin"
                st.toast("Autenticação bem-sucedida!")
                st.switch_page(CHAT_PAGE)
            else:
                st.error('Usuário ou senha incorretos')
