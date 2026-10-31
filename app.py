
print("================================")
print("       NOC SMART ASSISTANT")
print("================================")

print("Bem-vindo ao assistente tecnico!")

problema = input("\nDescreva o problema: ")

print("\nAnalisando sua solicitacao...")

if "lenta" in problema.lower():
    print("Orientacao: verificar a conexao e realizar testes de velocidade.")

elif "sem internet" in problema.lower():
    print("Orientacao: verificar o estado da conexao e encaminhar para analise tecnica.")

elif "ont" in problema.lower():
    print("Orientacao: verificar o cadastro e o estado da ONT.")

else:
    print("Problema nao identificado. Encaminhar para analise do NOC.")

print("\nAtendimento finalizado.")
