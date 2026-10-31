
from buscar_conhecimento import buscar

# CONJUNTO DE TESTES
testes = [
    {
        "pergunta": "O que é uma ONU?",
        "esperado": "EQ001"
    },
    {
        "pergunta": "Explique o funcionamento da ONU",
        "esperado": "EQ001"
    },
    {
        "pergunta": "O que é uma ONT?",
        "esperado": "EQ002"
    },
    {
        "pergunta": "Para que serve uma ONT?",
        "esperado": "EQ002"
    },
    {
        "pergunta": "Qual a diferença entre ONU e ONT?",
        "esperado": "EQ003"
    },
    {
        "pergunta": "Compare ONU e ONT",
        "esperado": "EQ003"
    },
    {
        "pergunta": "Como configurar uma VLAN no equipamento XYZ?",
        "esperado": None
    },
    {
        "pergunta": "Como alterar a senha do roteador ABC?",
        "esperado": None
    },
    {
        "pergunta": "Qual o procedimento para configurar BGP?",
        "esperado": None
    },
    {
        "pergunta": "Como acessar o sistema interno do provedor?",
        "esperado": None
    }
]

aprovados = 0
falhas = []

print("\n=== AVALIACAO DO MECANISMO DE BUSCA ===\n")

for numero, teste in enumerate(testes, start=1):
    resultados = buscar(teste["pergunta"])

    encontrado = (
        resultados[0]["id"]
        if resultados
        else None
    )

    if encontrado == teste["esperado"]:
        print(f"[OK] Teste {numero}: {teste['pergunta']}")
        aprovados += 1
    else:
        print(f"[FALHA] Teste {numero}: {teste['pergunta']}")
        print(f"   Esperado: {teste['esperado']}")
        print(f"   Encontrado: {encontrado}")

        falhas.append({
            "pergunta": teste["pergunta"],
            "esperado": teste["esperado"],
            "encontrado": encontrado
        })

total = len(testes)
taxa = (aprovados / total) * 100

print("\n=== RESULTADO FINAL ===")
print(f"Testes aprovados: {aprovados}/{total}")
print(f"Taxa de acerto: {taxa:.1f}%")

if falhas:
    print("\nPerguntas que precisam de melhorias:")

    for falha in falhas:
        print(f"- {falha['pergunta']}")
else:
    print("\nTodos os testes passaram!")
