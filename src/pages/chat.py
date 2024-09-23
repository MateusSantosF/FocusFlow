import streamlit as st
from src.configs.open_ai_config import build_chat_engine
from streamlit_feedback import streamlit_feedback

# Função para inicializar o agente usando cache para evitar recriações a cada interação
@st.cache_resource(ttl=3600)
def init_chat_engine():
    agent = build_chat_engine()
    return agent

# Inicializar o agente
chat_engine = init_chat_engine()

# Definir o título da aplicação
st.title("Tutor Virtual", anchor=False)

if "firts_run" not in st.session_state.keys():
    st.session_state.firts_run = True

if "messages" not in st.session_state.keys(): 
    st.session_state.messages = [ {"role": "assistant", "content": "Olá! Como posso ajudar?"}]

if prompt := st.chat_input(max_chars=300, placeholder="Digite sua pergunta"): 
    st.session_state.messages.append({"role": "user", "content": prompt})

def test(test):
    print(st.session_state.get("run_id") != None)
    print("==================")
    print(test)

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            st.session_state.firts_run = False
            response = chat_engine.chat(prompt)
            st.write(response.response)
            st.session_state.run_id = 1
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history

if st.session_state.firts_run == False:
    feedback = streamlit_feedback(
        align="flex-start",
        on_submit=test,
        feedback_type="thumbs",
        optional_text_label="[Opcional] Por favor explique o motivo da sua avaliação:"
    )