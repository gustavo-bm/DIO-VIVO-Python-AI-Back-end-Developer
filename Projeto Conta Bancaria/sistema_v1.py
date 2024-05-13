saldo = 0
qtdSaques = 0
extrato = []
LIMITE_SAQUES = 3

def fazerDeposito():
    valorDeposito = float(input("Valor do depósito: "))
    print()
    extrato.append(valorDeposito)
    print("Depósito realizado!")
    return valorDeposito

def fazerSaque():
    global saldo, qtdSaques
    if (qtdSaques == LIMITE_SAQUES):
        print("Limite máximo de saques atingido!")
        return
    valorSaque = float(input("Quanto deseja sacar? (Limite = 500): "))
    if (valorSaque > saldo):
        print("Ops! Saldo insuficiente...")
    else:
        if (valorSaque <= 500):
            saldo -= valorSaque
            print(f"Você sacou {valorSaque} reais e agora possui {saldo} reais em sua conta.")
            qtdSaques += 1
        else:
            print("Valor acima do limite!")

def mostrarExtrato():
    if extrato:
        for i, deposito in enumerate(extrato, start=1):
            print(f"Depósito {i}: {deposito}")
    else:
        print("Ainda não foram realizados depósitos!")

print(
        '''
    __________________________________________________________________
        
            Bem-vindo ao sistema bancário GBM!

            Digite:

            1 - Para realizar um Depósito
            2 - Para realizar um Saque
            3 - Para mostrar seu Extrato
            4 - Para sair

    __________________________________________________________________

        ''')

while True:
    operacao = int(input("Qual operação deseja realizar? "))
    if operacao == 4:
        break

    print()

    if operacao == 1: 
        saldo += fazerDeposito()
    elif operacao == 2:
        fazerSaque()
    elif operacao == 3:
        mostrarExtrato()