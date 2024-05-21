from abc import ABC, abstractmethod
from datetime import datetime

# Convenções: _ antes de atributo privado
#           @classmethod para criar um método de classe
#           @property para definir getters 

class Conta:
    def __init__(self, cliente, numero):
        self._limite_saques = 3
        self._num_saques = 0
        self._cliente = cliente
        self._agencia = "0001"
        self._numero = numero
        self._saldo = 0
        self._historico = Historico() 

    @classmethod
    def nova_conta(cls, cliente, numero):
        # cria e retorna nova instância da classe passada, a classe Conta
        return cls(cliente, numero)
    
    # definir getters
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        if valor > self._saldo:
            print("Ops! Saldo insuficiente...\n\n")
            return False
        elif valor <= 0:
            print("Valor inválido!\n\n")
            return False
        else:
            self._saldo -= valor
            print(f"Você sacou {valor} reais e agora possui R${self._saldo} em sua conta.\n\n")
            return True

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Você depositou {valor} reais e agora possui R${self._saldo} em sua conta.\n\n")
            return True
        else:
            print("Valor inválido!\n\n")
            return False

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques
    
    def sacar(self, valor):
        num_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])
        
        if num_saques >= self._limite_saques:
            print("Limite máximo de saques atingido! Lembre-se, você só pode realizar 3 saques por dia.\n\n")
            return False
        if valor > self._limite:
            print("Valor acima do limite de 500 reais por saque!\n\n")
            return False
        else:
            return super().sacar(valor)
    
    # método para exibição de dados padrão
    def __str__(self):
        return f"""\
Agência:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}
        """

# Interface 
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Historico:
    def __init__(self):
        self._transacoes = []
        
    # método getter
    @property
    def transacoes(self):
        return self._transacoes

    # adiciona uma transação no histórico, que nada mais é que uma lista
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    # método getter
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    # método getter
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Cliente:
    def __init__(self, nome, endereco):
        self._nome = nome
        self._endereco = endereco
        self._contas = []
        
    @property
    def nome(self):
        return self._nome

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(nome, endereco)
        self._cpf = cpf
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def data_nascimento(self):
        return self._data_nascimento

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

def depositar(conta):
    valor = float(input("Informe o valor para depósito: "))
    transacao = Deposito(valor)
    transacao.registrar(conta)

def sacar(conta):
    valor = float(input("Informe o valor para saque: "))
    transacao = Saque(valor)
    transacao.registrar(conta)

def exibir_extrato(conta):
    print(f"\nSaldo:            R$ {conta.saldo:.2f}")
    for transacao in conta.historico.transacoes:
        print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")

def cadastrar_usuario(usuarios):
    cpf = input("CPF (somente números): ")
    usuario = checar_usuario(cpf, usuarios)

    if usuario:
        print(f"CPF já cadastrado para o usuário {usuario.nome}, informe um CPF novo!\n\n")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento: ")
    endereco = input("Endereço (logradouro, num - bairro - cidade/sigla estado): ")

    novo_usuario = PessoaFisica(cpf, nome, data_nascimento, endereco)
    usuarios.append(novo_usuario)

    print("\nUsuário cadastrado!\n\n")

def checar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = checar_usuario(cpf, clientes)

    if cliente:
        print("\nJá existe cliente com esse CPF!\n\n")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
    clientes.append(cliente)

    print("\nCliente criado com sucesso!\n\n")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = checar_usuario(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado! Crie um usuário antes de criar uma conta.\n\n")
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\nConta criada com sucesso!\n\n")

def listar_contas(contas):
    for conta in contas:
        print(conta)

def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        if opcao == 'q':
            break

        print()
        if opcao == 'd':
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)
            if conta:
                depositar(conta)
            else:
                print("\nConta não encontrada!\n\n")
        elif opcao == 's':
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)
            if conta:
                sacar(conta)
            else:
                print("\nConta não encontrada!\n\n")
        elif opcao == 'e':
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)
            if conta:
                exibir_extrato(conta)
            else:
                print("\nConta não encontrada!\n\n")
        elif opcao == "nu":
            cadastrar_usuario(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)

main()
