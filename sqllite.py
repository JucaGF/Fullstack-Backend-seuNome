import sqlite3

# Função responsável por executar qualquer comando SQL no banco, com seu parâmetro sendo uma string com o cóodigo SQL
def run_sql(sql: str):
    # Abre (ou cria, se não existir) o banco de dados users.db
    con = sqlite3.connect("users.db")

    # Cria um cursor, que é o objeto que executa os comandos SQL
    cur = con.cursor()

    # Executa o código SQL recebido como string
    res = cur.execute(sql)

    # Busca todos os resultados retornados pelo comando, detalhe que para comandos de inserção de valores geralmente retorna uma lista vazia 
    data = res.fetchall()

    #Confirma as alterações feitas no banco
    con.commit()

    #retorna as informações
    return data
