import streamlit as st
from src.pages.fragments.access_code_frag import access_management_fragment
from src.utils.local_storage_utils import get_from_local_storage, set_to_local_storage

st.title("Configurações", anchor=False)
# Carregar as configurações do Local Storage
tratamento_default = get_from_local_storage('tratamento')
resposta_ia_default = get_from_local_storage('resposta_ia')

# Inicializar as configurações no session_state se ainda não estiver presente
if "configuracoes" not in st.session_state:
    st.session_state.configuracoes = {
        "tratamento": tratamento_default,
        "resposta_ia": resposta_ia_default
    }

# Atualizar as configurações no session_state com os valores do Local Storage
st.session_state.configuracoes["tratamento"] = tratamento_default
st.session_state.configuracoes["resposta_ia"] = resposta_ia_default

access_management_fragment()
# Cria o formulário para configurações

st.subheader("Experiência do Usuário", anchor=False)
with st.form(key="form_configuracoes"):
    tratamento = st.text_area(
        "O que gostaria que o Chat soubesse sobre si para lhe disponibilizar melhores respostas?",
        max_chars=300,
        placeholder="Exemplo: Trate-me de forma amigável e respeitosa.",
        value=st.session_state.configuracoes.get("tratamento", "")
    )
    resposta_ia = st.text_area(
        "De que forma gostaria que o Chat respondesse?",
        max_chars=300,
        placeholder="Exemplo: Responda de maneira clara e concisa.",
        value=st.session_state.configuracoes.get("resposta_ia", "")
    )
    submit_button = st.form_submit_button(label="Salvar Configurações")
    if submit_button:
        # Atualiza o session_state com as novas configurações
        tratamento_salvo = tratamento[:300]
        resposta_ia_salvo = resposta_ia[:300]

        st.session_state.configuracoes["tratamento"] = tratamento_salvo
        st.session_state.configuracoes["resposta_ia"] = resposta_ia_salvo

        # Salvar as configurações no Local Storage
        set_to_local_storage('tratamento', tratamento_salvo)
        set_to_local_storage('resposta_ia', resposta_ia_salvo)

        st.success("Configurações salvas com sucesso!")
