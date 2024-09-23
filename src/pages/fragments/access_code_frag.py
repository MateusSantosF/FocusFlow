import streamlit as st

from src.utils.auth import carregar_config, salvar_config

@st.fragment
def access_management_fragment():
    if st.session_state.authenticated_role == "admin":
        if st.session_state['authentication_status']:
            config = carregar_config()

            st.subheader("Código de acesso para alunos", anchor=False)
            with st.form(key="form_codigo_aluno"):
                novo_codigo = st.text_input(label="Digite o novo código de acesso para os alunos:", max_chars=12, placeholder="ex. 123456", value=config.get('acesso_aluno', ""))
                if st.form_submit_button("Atualizar Código"):
                    if novo_codigo:
                        config['acesso_aluno'] = str(novo_codigo)
                        salvar_config(config)
                        st.success("Código de acesso atualizado com sucesso!")
                    else:
                        st.error("Por favor, insira um código válido.")