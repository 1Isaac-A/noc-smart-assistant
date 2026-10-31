
from ollama import chat

# BASE DE CONHECIMENTO FICTICIA
conhecimento = """
ONT significa Optical Network Terminal.
E o equipamento que termina a conexao de fibra optica
no local do assinante e permite a comunicacao com a
rede do provedor.

Uma conexao Wi-Fi ativa nao garante que o dispositivo
tenha acesso a internet.

Problemas de lentidao podem ter diferentes causas.
A analise pode envolver testes de velocidade,
verificacao da conexao e avaliacao dos equipamentos.
"""

print("=== NOC SMART ASSISTANT COM IA ===")

pergunta = input("\nDigite sua pergunta: ")

resposta = chat(
    model="llama3.2:1b",
    messages=[
        {
            "role": "system",
            "content": (
                "Voce e um assistente educacional de telecomunicacoes. "
                "Responda em portugues brasileiro. "
                "Utilize somente as informacoes da base abaixo. "
                "Se a base nao contiver a resposta, diga que "
                "nao possui informacoes suficientes. "
                "Nao invente siglas ou procedimentos.\n\n"
                f"BASE DE CONHECIMENTO:\n{conhecimento}"
            )
        },
        {
            "role": "user",
            "content": pergunta
        }
    ],
    options={
        "temperature": 0
    }
)

print("\nResposta da IA:")
print(resposta.message.content)
