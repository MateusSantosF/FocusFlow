import streamlit as st

from src.services.supabase_services import SUPABASE_CLIENT

st.cache_data(ttl=60)
def get_current_config():
    result = SUPABASE_CLIENT.schema("public").table("access_configs").select("*").execute()
    config = result.data[0]
    current_access_code = config['access_code']
    return current_access_code

current_access_code = get_current_config()

@st.fragment
def access_management_fragment():
    if st.session_state.authenticated_role == "admin":
        if st.session_state['authentication_status']:

            st.subheader("Código de acesso para alunos", anchor=False)
            with st.form(key="form_codigo_aluno"):
                novo_codigo = st.text_input(label="Digite o novo código de acesso para os alunos:", max_chars=12, placeholder="ex. 123456", value=current_access_code)
                if st.form_submit_button("Atualizar Código"):
                    if novo_codigo:
                        result = SUPABASE_CLIENT.schema("public").table("access_configs").upsert({ "id": 1, "access_code":  novo_codigo}).execute()
                        st.success("Código de acesso atualizado com sucesso!")
                    else:
                        st.error("Por favor, insira um código válido.")