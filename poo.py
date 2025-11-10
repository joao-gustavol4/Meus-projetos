'''''class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def falar(self):
        print(f"")

p1 = Pessoa("João", 17)

print(p1.nome, p1.idade)
'''

class Carro:
    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano

    def descrever(self):
        print(f"A {self.marca} em {self.ano}, lançou um novo modelo do {self.modelo}")    

c1 = Carro("chevrolet", "onix", 2019)
c1.descrever()  