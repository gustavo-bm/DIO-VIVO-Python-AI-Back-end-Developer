import pandas as pd
import random

LIMITE_SAQUES = 3

saldo = 0
qtdSaques = 0
usuarios = {}
extrato = {}

nome = str(input("Qual o seu nome? "))
numConta = random.randint(100, 999)
usuarios[nome] = {"nome": nome, "conta": numConta}

def fazerDeposito():
    global saldo
    valorDeposito = float(input("Valor do depósito: "))
    print("Depósito realizado!")
    if "Depósito" in extrato:
        extrato["Depósito"].append(valorDeposito)
    else:
        extrato["Depósito"] = [valorDeposito]
    saldo += valorDeposito
    return valorDeposito

def fazerSaque():
    global saldo, qtdSaques
    if qtdSaques == LIMITE_SAQUES:
        print("Limite máximo de saques atingido!")
        return
    
    valorSaque = float(input("Quanto deseja sacar? (Limite = 500): "))
    if valorSaque > saldo:
        print("Ops! Saldo insuficiente...")
    else:
        if valorSaque <= 500:
            saldo -= valorSaque
            print(f"Você sacou {valorSaque} reais e agora possui {saldo} reais em sua conta.")
            if "Saque" in extrato:
                extrato["Saque"].append(valorSaque)
            else:
                extrato["Saque"] = [valorSaque]
            qtdSaques += 1
        else:
            print("Valor acima do limite!")

def mostrarExtrato():
    if extrato:
        for chave, valores in extrato.items():
            for i, valor in enumerate(valores):
                print(f"{chave} {i+1}: {valor} reais")
    else:
        print("Ainda não foram realizados depósitos ou saques!")

print(
        f'''
    __________________________________________________________________
        
            Bem-vindo ao sistema bancário GBM, {nome}!

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
        fazerDeposito()
    elif operacao == 2:
        fazerSaque()
    elif operacao == 3:
        mostrarExtrato()
