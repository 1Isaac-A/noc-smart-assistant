
import json
import re
import unicodedata
from pathlib import Path

# LOCALIZACAO DO ARQUIVO JSON
caminho = (
    Path(__file__).parent
    / "base_conhecimento"
    / "equipamentos.json"
)

# CARREGAR DOCUMENTOS
with open(caminho, "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

documentos = dados["documentos"]


# NORMALIZAR TEXTO
def normalizar(texto):
    texto = texto.lower()

    texto = "".join(
        letra
        for letra in unicodedata.normalize("NFD", texto)
        if unicodedata.category(letra) != "Mn"
    )

    return texto


# VERIFICAR EXPRESSAO COMPLETA
def contem_expressao(texto, expressao):
    padrao = (
        r"(?<!\w)"
        + re.escape(expressao)
        + r"(?!\w)"
    )

    return re.search(padrao, texto) is not None


# BUSCAR DOCUMENTO MAIS RELEVANTE
def buscar(pergunta):
    pergunta_normalizada = normalizar(pergunta)

    resultados = []

    for documento in documentos:
        pontuacao = 0

        for palavra_chave in documento["palavras_chave"]:
            chave = normalizar(palavra_chave)

            if contem_expressao(
                pergunta_normalizada, chave
            ):
                # Expressao mais especifica recebe mais pontos
                quantidade_palavras = len(chave.split())

                pontuacao += 10 * quantidade_palavras

        if pontuacao > 0:
            resultados.append({
                "documento": documento,
                "pontuacao": pontuacao
            })

    # ORDENAR POR RELEVANCIA
    resultados.sort(
        key=lambda item: item["pontuacao"],
        reverse=True
    )

    # RETORNAR APENAS O MAIS RELEVANTE
    if resultados:
        return [resultados[0]["documento"]]

    return []


# TESTE PELO TERMINAL
if __name__ == "__main__":
    pergunta = input("Digite sua pergunta: ")

    resultados = buscar(pergunta)

    if resultados:
        print("\nDocumentos encontrados:")

        for documento in resultados:
            print(f"\nID: {documento['id']}")
            print(f"Titulo: {documento['titulo']}")
            print(f"Conteudo: {documento['conteudo']}")

    else:
        print(
            "\nNenhum documento encontrado na base."
        )
