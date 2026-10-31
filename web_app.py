
import streamlit as st
from ollama import chat
from buscar_conhecimento import buscar


# ==========================================
# CONFIGURACAO DA PAGINA
# ==========================================

st.set_page_config(
    page_title="NOC Smart Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 NOC Smart Assistant")

st.caption(
    "Versão 1.0 - Assistente híbrido com IA e respostas validadas"
)

st.write(
    "Assistente educacional de suporte técnico "
    "para provedores de internet."
)

st.divider()


# ==========================================
# INICIALIZAR HISTORICO
# ==========================================

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []


# ==========================================
# EXIBIR MENSAGENS
# ==========================================

def exibir_mensagem(mensagem):

    with st.chat_message(mensagem["role"]):

        st.markdown(mensagem["content"])

        # IDENTIFICAR MODO DA RESPOSTA
        modo = mensagem.get("modo")

        if modo == "validado":
            st.caption(
                "✅ Resposta validada na base de conhecimento"
            )

        elif modo == "gerado":
            st.caption(
                "🤖 Resposta gerada por IA com base na documentação"
            )

        # MOSTRAR FONTES
        fontes = mensagem.get("fontes", [])

        if fontes:

            with st.expander("📚 Fontes consultadas"):

                for fonte in fontes:
                    st.write(
                        f"{fonte['id']} - {fonte['titulo']}"
                    )

        # MOSTRAR STATUS
        status = mensagem.get("status")

        if status == "sem_documentacao":
            st.caption(
                "Nenhum documento correspondente "
                "foi encontrado na base de conhecimento."
            )

        elif status == "erro":
            st.caption(
                "Ocorreu um erro ao consultar o modelo de IA."
            )


# ==========================================
# MOSTRAR HISTORICO
# ==========================================

for mensagem in st.session_state.mensagens:
    exibir_mensagem(mensagem)


# ==========================================
# CAMPO DE PERGUNTA
# ==========================================

pergunta = st.chat_input(
    "Digite sua dúvida técnica..."
)


if pergunta:

    # SALVAR MENSAGEM DO USUARIO
    mensagem_usuario = {
        "role": "user",
        "content": pergunta
    }

    st.session_state.mensagens.append(
        mensagem_usuario
    )

    exibir_mensagem(mensagem_usuario)

    # ======================================
    # BUSCAR CONHECIMENTO
    # ======================================

    documentos = buscar(pergunta)

    fontes = [
        {
            "id": documento["id"],
            "titulo": documento["titulo"]
        }
        for documento in documentos
    ]

    # ======================================
    # CASO 1: SEM DOCUMENTACAO
    # ======================================

    if not documentos:

        mensagem_ia = {
            "role": "assistant",
            "content": (
                "Não encontrei documentação suficiente "
                "na base de conhecimento para responder "
                "a essa pergunta.\n\n"
                "Consulte documentação técnica validada "
                "antes de realizar procedimentos."
            ),
            "fontes": [],
            "status": "sem_documentacao",
            "modo": None
        }

    else:

        documento_principal = documentos[0]

        # ==================================
        # CASO 2: RESPOSTA VALIDADA
        # ==================================

        resposta_validada = documento_principal.get(
            "resposta_validada"
        )

        if resposta_validada:

            mensagem_ia = {
                "role": "assistant",
                "content": resposta_validada,
                "fontes": fontes,
                "status": "documentado",
                "modo": "validado"
            }

        # ==================================
        # CASO 3: RESPOSTA GERADA POR IA
        # ==================================

        else:

            contexto = "\n\n".join(
                documento["conteudo"]
                for documento in documentos
            )

            with st.spinner("Consultando a IA..."):

                try:

                    resposta = chat(
                        model="qwen2.5:1.5b",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Voce e um assistente tecnico "
                                    "educacional especializado "
                                    "em telecomunicacoes.\n\n"

                                    "REGRAS:\n"
                                    "1. Responda em portugues brasileiro.\n"
                                    "2. Utilize somente os documentos "
                                    "fornecidos.\n"
                                    "3. Nao utilize conhecimento externo.\n"
                                    "4. Nao invente siglas, comandos, "
                                    "procedimentos ou caracteristicas.\n"
                                    "5. Seja claro, objetivo e evite "
                                    "repeticoes.\n"
                                    "6. Prefira respostas curtas, "
                                    "de ate 100 palavras.\n"
                                    "7. Se a informacao for insuficiente, "
                                    "reconheca a limitacao.\n\n"

                                    f"DOCUMENTOS:\n{contexto}"
                                )
                            },
                            {
                                "role": "user",
                                "content": pergunta
                            }
                        ],
                        options={
                            "temperature": 0,
                            "num_ctx": 2048,
                            "num_predict": 180
                        }
                    )

                    mensagem_ia = {
                        "role": "assistant",
                        "content": resposta.message.content,
                        "fontes": fontes,
                        "status": "documentado",
                        "modo": "gerado"
                    }

                except Exception as erro:

                    mensagem_ia = {
                        "role": "assistant",
                        "content": (
                            "Não foi possível consultar a IA. "
                            "Verifique se o Ollama está funcionando."
                        ),
                        "fontes": [],
                        "status": "erro",
                        "modo": None
                    }

                    st.error(str(erro))

    # ======================================
    # SALVAR E MOSTRAR RESPOSTA
    # ======================================

    st.session_state.mensagens.append(
        mensagem_ia
    )

    exibir_mensagem(mensagem_ia)


# ==========================================
# LIMPAR CONVERSA
# ==========================================

st.divider()

if st.button("🗑️ Limpar conversa"):

    st.session_state.mensagens = []

    st.rerun()


# ==========================================
# RODAPE
# ==========================================

st.caption(
    "Projeto educacional com dados fictícios. "
    "As respostas geradas por IA devem ser verificadas "
    "antes de qualquer aplicação em redes reais."
)
