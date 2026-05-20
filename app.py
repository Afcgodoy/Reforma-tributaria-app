import streamlit as st
from openai import OpenAI
import time
import os


# Inicialize o cliente OpenAI com sua chave de API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
    
    resposta = client.responses.create(
        model="gpt-5.5",
        instructions="Você é um assistente útil que utiliza o vetor de arquivos para responder perguntas com base nos documentos fornecidos. Forneça respostas claras e precisas, além de muito bem explicadas, pois você estará respondendo perguntas feitas por empresas que querem acompanhar o que mudou com a reforma tributária. Sempre indique o dispositivo legal e o inciso (se tiver) que usou para responder, e, sempre que encontrar contradiçõe nos arquivos que usou como base para responder, você deve informar. Saiba que você precisa seguir uma hierarquia de arquivos para procurar as respostas: Primeiro procure na emenda constitucional 132/2023, depois nas leis complementares 214/2025 e 227/2026, depois nas leis complementarem 224/2025, 225/2026 e 229/2026, depois no decreto 12955/2026 e na resolução cgIBS 6/2026, e por ultimo nos demais arquivos que estão no vetor anexado mas que não foram mencionados aqui.",
        input=user_input,
        reasoning={
            "effort": "medium"
        },
        
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [vector_store_id]
            }
        ],
        tool_choice="auto"
    )

   # Recupere a resposta do assistente
    if resposta and resposta.output_text:
        response = resposta.output_text
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
            
    else:
        st.error("Erro: Não foi possível obter uma resposta.")
