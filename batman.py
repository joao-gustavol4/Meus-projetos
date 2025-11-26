import sqlite3

class BancoDeDados:
    def __init__(self, caminho: str = "batman.db"):
        self.caminho = caminho

    def conexao(self):
        return sqlite3.connect(self.caminho)
    

class Tabelas:
    def __init__(self, banco: BancoDeDados):
        self.banco = banco
    
    def criar(self):
        conexao = self.banco.conexao()
        cursor = conexao.cursor()

        sql = """
        CREATE TABLE IF NOT EXISTS resultados(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operacao TEXT,
            valor1 REAL,
            valor2 REAL,
            resultado REAL
        )
        """

        cursor.execute(sql)
        conexao.commit()
        conexao.close()


class Calculadora:
    def __init__(self, banco: BancoDeDados):
        self.banco = banco

    def salvar(self, op, x, y, resultado):
        conexao = self.banco.conexao()
        cursor = conexao.cursor()

        cursor.execute(
            "INSERT INTO resultados (operacao, valor1, valor2, resultado) VALUES (?, ?, ?, ?)",
            (op, x, y, resultado)
        )

        conexao.commit()
        conexao.close()

    def soma(self, x, y):
        return x + y
    
    def sub(self, x, y):
        return x - y
    
    def multi(self, x, y):
        return x * y
    
    def div(self, x, y):
        if y == 0:
            print("Erro: não existe divisão por zero!")
            return None
        return x / y


# principal
if __name__ == "__main__":
    banco = BancoDeDados()
    tabela = Tabelas(banco)
    tabela.criar()

    calc = Calculadora(banco)

    while True:
        print("The CALCULATOR")
        print("Digite a operação:")
        print("1 - Soma")
        print("2 - Subtração")
        print("3 - Multiplicação")
        print("4 - Divisão")
        print("0 - Sair")

        escolha = input("Escolha: ")

        if escolha == "0":
            print("sai daqui")
            break  # sai do while

        if escolha not in ["1", "2", "3", "4"]:
            print("Opção inválida!")
            continue  # volta ao início do loop

        # pegar os valores
        x = float(input("Digite o primeiro valor: "))
        y = float(input("Digite o segundo valor: "))

        # realizar operação
        if escolha == "1":
            op = "soma"
            resultado = calc.soma(x, y)

        elif escolha == "2":
            op = "sub"
            resultado = calc.sub(x, y)

        elif escolha == "3":
            op = "multi"
            resultado = calc.multi(x, y)

        elif escolha == "4":
            op = "div"
            resultado = calc.div(x, y)
            if resultado is None:
                continue  # volta ao início sem salvar

        # mostrar resultado
        print(f"\nResultado: {resultado}\n")

        # salvar no banco
        calc.salvar(op, x, y, resultado)
        print("Resultado salvo no banco de dados!")
