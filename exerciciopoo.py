# Parte 1
'''class Pessoa():
    def __init__(self, nome: str, idade: int):
        self.nome = nome
        self.idade = idade
    
    def apresentar(self):
        print(f"Olá, meu nome é {self.nome} e tenho {self.idade} anos.")

p1 = Pessoa("Kamila", 16)
p1.apresentar()'''

 # 2 exercicio.

'''class Livro():
    def __init__(self, titulo: str, autor:str, preco: float):
        self.titulo = titulo
        self.autor = autor
        self.preco = preco
    
    def info(self):
        print(f"O livro {self.titulo}, escrito por {self.autor} custa {self.preco}")

l = Livro("Harry Potter", "J.K rowling", 39.90)
l.info()'''

# 3 exercico

'''class Carro():
    def __init__(self, modelo: str, cor: str):
        self.modelo = modelo
        self.cor = cor
        
    def dirigir(self):
        print(f"O carro do modelo {self.modelo} da cor {self.cor} está em movimento")

c = Carro("Uno", "Escada em cima")
c.dirigir()'''

# Parte 2 
# 4 exercicio

class Aluno():
    def __init__(self, nome: str):
        self.nome = nome
        self.notas = []
    
    def coletar_notas(self):
        # Pergunta quantas notas serao inseridas e faz a leitura de cada uma.
        qnt = int(input(f"Quantas notas serão inseridas para {self.nome}?"))
        # Limpo a lista caso a função seja chamada mais de uma vez
        self.notas.clear()

        # Lê cada nota e adiciona na lista ( A variavel qnt decide quantas vezes isso repete )
        for i in range(qnt):
            nota = float(input(f"Digite a {i + 1} nota: "))
            # O comando "append" insere valores no ultimo lugas da lista,  preservando os anteriores
            self.notas.append(nota)
    
    def media(self):
        # retornar a media das notas
        if not self.notas:
            return 0.0
        else:
            return sum(self.notas) / len(self.notas)
        
    def situacao(self):
        # retornar "Aprovado" ou "Reprovado" com base na media.
        m = self.media()
        return "Aprovado" if m >= 7 else "Reprovado"


nome = input("Digite o nome do aluno: ")
aluno = Aluno(nome)

aluno.coletar_notas()

print(" Esse é o seu RESULTADO ")
print(f"Aluno: {aluno.nome}")
print(f"Média: {aluno.media()}")
print(f"Situação: {aluno.situacao()}")