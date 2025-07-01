def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato, numero_saques

    if numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        return saldo, extrato, numero_saques

    if valor > limite:
        print(f"Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}.")
        return saldo, extrato, numero_saques

    # Calcular a taxa de serviço (1.5% do valor do saque)
    taxa_servico = valor * 0.015
    valor_total_saque = valor + taxa_servico

    if valor_total_saque > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return saldo, extrato, numero_saques

    saldo -= valor_total_saque
    extrato.append(f"Saque: R$ {valor:.2f} (Taxa de serviço: R$ {taxa_servico:.2f})")
    numero_saques += 1
    print(f"Saque de R$ {valor:.2f} realizado com sucesso! Taxa de serviço de R$ {taxa_servico:.2f} aplicada.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n---------- EXTRATO ----------")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for movimento in extrato:
            print(movimento)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("-----------------------------\n")

def menu():
    print("""
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
""")
    return input("=> ").strip().lower()

# Variáveis globais para o sistema
saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = menu()

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = depositar(saldo, valor, extrato)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato, numero_saques = sacar(saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES)

    elif opcao == "e":
        exibir_extrato(saldo, extrato)

    elif opcao == "q":
        print("Obrigado por usar nosso sistema bancário. Até mais!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
