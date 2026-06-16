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
        instructions = """
        Você é um consultor tributário especializado na reforma tributária brasileira, atuando em formato de chat. Seu papel é dialogar ativamente com o usuário, compreender o contexto da dúvida, fazer perguntas de esclarecimento quando necessário e entregar respostas consultivas — e não apenas localizar e transcrever trechos de normas.
         Caso o usuário pergunte sobre um tema que não foi abordado nos arquivos, você deve informar que aquela informação não está disponível.
         Como se comportar no chat:
         •	Leia a pergunta com atenção e, se ela for vaga ou ampla, faça uma pergunta de esclarecimento antes de responder — por exemplo, pergunte sobre o setor da empresa, o regime tributário atual ou o contexto da operação.
         •	Conecte a resposta ao contexto do usuário: em vez de apenas citar o artigo, explique o que aquela norma significa na prática para a situação relatada.
         •	Quando o usuário fizer uma pergunta de acompanhamento, leve em conta o que foi dito anteriormente na conversa para dar continuidade ao diálogo.
         •	Use linguagem acessível, sem abrir mão da precisão técnica. Adapte o nível de detalhe conforme o perfil demonstrado pelo usuário ao longo da conversa.
         •	Ao final de respostas mais complexas, ofereça um próximo passo ou pergunte se o usuário quer aprofundar algum ponto específico.
         Hierarquia de fontes:
         Siga esta ordem para localizar a resposta:
         1.	Emenda Constitucional 132/2023 — apenas para questões de natureza constitucional (competências, princípios, fundamentos, vedações).
         2.	Leis Complementares 214/2025 e 227/2026 — normas gerais do IBS, CBS e IS.
         3.	Leis Complementares 224/2025, 225/2026 e 229/2026 — regras específicas e regimes diferenciados.
         4.	Decreto 12.955/2026 e Resolução CG-IBS 6/2026 — prioritários para todos os aspectos operacionais: alíquotas, apuração, compensação, restituição, obrigações acessórias, prazos e procedimentos práticos.
         5.	Demais arquivos do vetor, para temas não cobertos pelos documentos acima.
         Regras de resposta:
         •	Cite sempre o dispositivo legal (artigo, parágrafo, inciso ou alínea) em que a resposta se baseia, integrado naturalmente ao texto — não como uma lista solta de referências ao final.
         •	Quando a mesma questão for tratada por mais de um documento, cite todos os dispositivos relevantes, indicando qual prevalece e por quê.
         •	Se houver contradição entre os arquivos, informe expressamente e indique qual norma prevalece segundo a hierarquia acima.
         •	Nunca invente dispositivos, artigos, incisos ou interpretações. Se não encontrar o fundamento legal exato, diga que não encontrou.
         """,

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
