import streamlit as st
from anthropic import Anthropic
import os

# Inicialize o cliente Anthropic com sua chave de API
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Título do app
st.title("Consulte a Reforma Tributária")

# Inicialize o estado da sessão para armazenar o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exiba o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de input para a pergunta do usuário
user_input = st.chat_input("Pergunta:")

if user_input:
    # Adicione a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Chame a API da Anthropic enviando todo o histórico da conversa
    # (a Anthropic é stateless: o "contexto" vem das mensagens que você envia)
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=4000,
        system="Você é um especialista em legislação tributária brasileira.",
        messages=st.session_state.messages,
    )

    # A resposta é texto simples — não precisa de json.loads
    resposta = response.content[0].text
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.markdown(resposta)
