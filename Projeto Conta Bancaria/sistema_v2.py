import textwrap

def menu():
    menu = f"""\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))
    
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("Depósito realizado!")
    else:
        print("Operação falhou, informe um valor acima de zero!")
        
    return saldo, extrato

def sacar(*, saldo, valor, qtde_saques, limite):
    if qtde_saques == limite:
        print("Limite máximo de saques atingido!")
        return
    
    valor = float(input("Quanto deseja sacar? (Limite = 500): "))
    if valor > saldo:
        print("Ops! Saldo insuficiente...")
    else:
        if valor <= 500:
            saldo -= valor
            extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            qtde_saques += 1
            
            print(f"Você sacou {valor} reais e agora possui {saldo} reais em sua conta.")
        else:
            print("Valor acima do limite!")

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com este CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, num_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

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
            criar_usuario(usuarios)

        elif opcao == "nc":
            num_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, num_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

main()