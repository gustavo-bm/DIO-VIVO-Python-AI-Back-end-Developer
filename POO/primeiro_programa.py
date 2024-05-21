class Bicicleta:
    def __init__(self, cor, modelo, ano, valor):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano
        self.valor = valor
        movimento = False
        
    def buzinar():
        print('Fon fon')
        
    def parar(self):
        self.movimento = False
    
    def correr(self):
        self.movimento = True
        

bike1 = Bicicleta('azul', 'caloi', 2023, 1500)
print(bike1.ano)