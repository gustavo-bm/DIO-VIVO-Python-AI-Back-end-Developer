import textwrap

def menu():
    print (f"""\n
    _______________ MENU _______________
    
    [d]     Depositar
    [s]     Sacar
    [e]     Extrato
    [nc]    Nova conta
    [lc]    Listar contas
    [nu]    Novo usuário
    [q]     Sair\n\n""")
    opcao = input("Opção: ")
    return opcao
    
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("Depósito realizado!\n\n")
    else:
        print("Operação falhou, favor informar um valor acima de zero.\n\n")
        
    return saldo, extrato

def sacar(*, saldo, valor, qtde_saques, limite):
    if qtde_saques == limite:
        print("Limite máximo de saques atingido! Lembre-se, você só pode realizar 3 saques por dia.\n\n")
        return
    
    valor = float(input("Quanto deseja sacar? (Limite = 500): "))
    if valor > saldo:
        print("Ops! Saldo insuficiente...\n\n")
    else:
        if valor <= 500:
            saldo -= valor
            extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            qtde_saques += 1
            
            print(f"Você sacou {valor} reais e agora possui {saldo} reais em sua conta.\n\n")
        else:
            print("Valor acima do limite!\n\n")

def exibir_extrato(saldo, /, *, extrato):
    if extrato:
        print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    else:
        print("Não ocorreram movimentações ainda!\n\n")

def cadastrar_usuario(usuarios):
    cpf = input("CPF (somente números): ")
    usuario = checar_usuario(cpf, usuarios)

    if usuario:
        print(f"CPF já cadastrado para o usuário {usuario['nome']}, informe um CPF novo!\n\n")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento: ")
    endereco = input("Endereço (logradouro, num - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário cadastrado!")

def checar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, num_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = checar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": num_conta, "usuario": usuario}

    print("\nUsuário não encontrado, favor criar o seu usuário antes.")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}\n
        """
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    saldo = 0
    numero_saques = 0
    extrato = ""
    usuarios = []
    contas = []
    
    while True:

        opcao = menu()
        if opcao == 'q':
            break
    
        print()

        if opcao == 'd':
            valor = float(input("Valor do depósito: "))
            saldo, extrato =depositar(saldo, valor, extrato)
            
        elif opcao == 's':
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                qtde_saques=numero_saques,
                limite=LIMITE_SAQUES,
            )
            
        elif opcao == 'e':
            exibir_extrato(saldo, extrato=extrato)
            
        elif opcao == "nu":
            cadastrar_usuario(usuarios)

        elif opcao == "nc":
            num_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, num_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

main()