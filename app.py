import streamlit as st
from anthropic import Anthropic
import time
import os


# Inicialize o cliente OpenAI com sua chave de API
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Título do app
st.title("Consulte a Reforma Tributária")

# Inicialize o estado da sessão para armazenar a thread e o histórico de mensagens
if "thread_id" not in st.session_state:
   thread = client.beta.threads.create()
   st.session_state.thread_id = thread.id
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

    vector_store_id = "vs_6a05bdf2078481919f6649982d19904e"
    
    response = client.beta.messages.create(
       model="claude-sonet-5",
       max_tokens=4000,
       system="""Você é um especialista em legislação tributária brasileira.""",
       messages=[
           {
               "role": "user",
               "content": user_input
           }
       ]
   )
   # Recupere a resposta do assistente

   dados = json.loads(response.content[0].text)

   st.session_state.messages.append({"role": "assistant", "content": dados})
   with st.chat_message("assistant"):
      st.markdown(dados)
      
