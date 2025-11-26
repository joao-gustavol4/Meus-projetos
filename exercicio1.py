import sqlite3 #importar o sqlite3 para o codigo

class BancoDeDados:
    def __init__(self, caminho_banco: str = "ex1_produtos.db"): # construtor criando o caminho para o banco de dados e definindo aquirvo que vai ser gerado
        self.caminho_banco = caminho_banco

    def conectar(self): #funçao para conexao entre o sqlite3 para o banco
        return sqlite3.connect(self.caminho_banco) # (.connect) = serve para fazer esse interligação
    
class RepositorioDeProdutos: # classe para fazer os espaços e categorias da tabela
        def __init__(self, banco: BancoDeDados): #funçao construtor que chama a classe BancoDeDados e define ela como a variavel banco
            self.banco = banco

        def criar_tabela(self): #funçao da criacao da tabela usando a lingugaem SQlite3
            conexao = self.banco.conectar() # variavel que chama a funçao da conexao
            cursor = conexao.cursor() #variavel que integra tudo e habilita as funcionalidades da funcao .cursor(delete,edit,execute etc)
            comando_criacao = """
            CREATE TABLE IF NOT EXISTS produtos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                preco REAL
            );
            """ #comando para a criacao da tabela definindo cada coisa que vai nela e os requerimentos de cada item(se é inteiro,text,real etc) utilizando outra linguagem de programação(sqlite3)
            cursor.execute(comando_criacao) #executanodo a criacao da tabela pro banco de dados
            conexao.commit() # o .commit serve para verificar se esta tudo certo  para a criacao do banco de dados
            conexao.close() # .close fecha todas essas ações do codigo encerrando-o, analogia(fechar a porta quando acabar a aula)

if __name__ == "__main__": #funcao para definir o banco de dados como algo principal do codigo(main)
    banco = BancoDeDados() # banco esta salvando o endereço da def BancoDeDados
    repositorio = RepositorioDeProdutos(banco)  #repositorio esta resumindo basicamente todas as funções do codigo de uma vez

    repositorio.criar_tabela() #execução da criaçao do banco de dados
    print("Tabela ta feita") #print de verificaçaõ
            

