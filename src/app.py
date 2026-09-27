import uuid
from pathlib import Path
import streamlit as st
import requests
from config import OLLAMA_URL, MODELO
from agente import SYSTEM_PROMPT, FUNCOES, tools

# === Configuração de sessão ===


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

session_id = st.session_state.session_id
session_dir=Path("Sessions") / session_id
try:
    session_dir.mkdir(parents=True)
except FileExistsError:
    print("Você está em uma sessão anterior. Clique no botão de novo chat para iniciar uma nova sessão")
    session_dir.mkdir(parents=True, exist_ok=True)

if "dataframes" not in st.session_state:
    st.session_state.dataframes = {}


#=== Chamar Ollama & funções ===
def perguntar(msg,status):
    messages=[
    {
        "role":"system",
        "content": SYSTEM_PROMPT
    },
    {
        "role": "user",
        "content": msg
    }
    ]

    while True:

        r = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELO,
                "messages": messages,
                "tools": tools,
                "stream": False
            }
        )


        data = r.json()
        mensagem = data["message"]

        messages.append(mensagem)

        if "tool_calls" not in mensagem:
            return mensagem["content"]

        for chamada in mensagem["tool_calls"]:

            nome = chamada["function"]["name"]
            argumentos = chamada["function"]["arguments"]

            status.write(
                f"🔧 Executando `{nome}`..."
            )
            funcao = FUNCOES[nome]
            resultado = funcao(
                **argumentos,   
                dataframes=st.session_state.dataframes,
                session_dir=session_dir
            )
            status.write(
                f"✓ `{nome}` concluída"
            )

            messages.append({
                "role": "tool",
                "content": resultado
            })

# === Interface ===

if st.button("Novo chat"):
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.dataframes = {}

    st.rerun()

st.title ("Aurora")

if pergunta:=st.chat_input("Em qual tarefa posso ajudar hoje?"):
    st.chat_message("user").write(pergunta)

    with st.chat_message("assistant"):

        with st.status(
            "Aurora está trabalhando...",
            expanded=True
        ) as status:

            resposta = perguntar(
                pergunta,
                status
            )

            status.update(
                label="Concluído",
                state="complete"
            )

        st.write(resposta)