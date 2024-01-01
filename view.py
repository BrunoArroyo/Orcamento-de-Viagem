# importando o SQLite
import sqlite3 as lite

# Criando a conexão
con = lite.connect('dados.db')

# Inserir quantia

def inserir_quantia(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Quantia (VALOR) VALUES(?)"
        cur.execute(query, i)

# Visualizar quantia total

def visualizar_quantia():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Quantia")
        row = cur.fetchall()

        for i in row:
            lista_itens.append(i)
        
    return lista_itens

# Atualizar quantidade

def atualizar_quantia_total(i):
    with con:
        cur = con.cursor()
        query = "UPDATE Quantia SET VALOR=? WHERE ID=?"
        cur.execute(query, i)

# Apagar segunda linha
        
def apagar_linha(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Quantia WHERE ID=?"
        cur.execute(query, (i,))

# Somente criei o código acima pois tinha rodado  inserir_quantia duas vezes sem querer

# Obter valor para aplicar na tela do sistema
def obter_valor_total():
    with con:
        cur = con.cursor()
        cur.execute("SELECT SUM(valor) FROM Quantia")
        resultado = cur.fetchone()
        return resultado[0] if resultado and resultado[0] is not None else 0.0
    
    
print(visualizar_quantia())