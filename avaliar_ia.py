
from ollama import chat
from buscar_conhecimento import buscar

# PERGUNTAS PARA AVALIACAO
perguntas = [
    "O que é uma ONU?",
    "Qual a diferença entre ONU e ONT?",
    "Como configurar uma VLAN no equipamento XYZ?"
]

print("\n=== AVALIACAO DA IA ===\n")

for numero, pergunta in enumerate(perguntas, start=1):

    print(f"\nTESTE {numero}")
    print(f"Pergunta: {pergunta}")

    # BUSCAR DOCUMENTOS
    documentos = buscar(pergunta)

    # CASO 1: NAO EXISTE DOCUMENTACAO
    if not documentos:
        print("Resultado: Sem documentacao.")
        print("IA nao consultada.")
        continue

    documento_principal = documentos[0]

    print("Fonte:", documento_principal["id"])

    # CASO 2: EXISTE RESPOSTA VALIDADA
    resposta_validada = documento_principal.get(
        "resposta_validada"
    )

    if resposta_validada:
        print("Modo: Resposta validada")
        print("\nResposta:")
        print(resposta_validada)

        # PULAR A CONSULTA AO QWEN
        continue

    # CASO 3: GERAR RESPOSTA COM IA
    contexto = "\n\n".join(
        documento["conteudo"]
        for documento in documentos
    )

    print("Modo: Resposta gerada por IA")

    try:
        resposta = chat(
            model="qwen2.5:1.5b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Voce e um assistente tecnico educacional.\n"
                        "Sua tarefa e explicar SOMENTE o conteudo "
                        "do documento fornecido.\n\n"

                        "REGRAS:\n"
                        "1. Nao utilize conhecimento externo.\n"
                        "2. Nao invente siglas ou definicoes.\n"
                        "3. Nao acrescente conceitos ausentes.\n"
                        "4. Prefira respostas curtas, de ate 100 palavras.\n"
                        "5. Se a pergunta pedir uma comparacao, "
                        "explique apenas as diferencas documentadas.\n"
                        "6. Se faltar informacao, diga que o documento "
                        "nao permite responder completamente.\n"
                        "7. Responda em portugues brasileiro.\n\n"

                        f"DOCUMENTO VALIDADO:\n{contexto}"
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

        print("\nResposta:")
        print(resposta.message.content)

    except Exception as erro:
        print(f"Erro ao consultar a IA: {erro}")

print("\n=== FIM DA AVALIACAO ===")
