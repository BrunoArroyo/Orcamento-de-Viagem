# importando o SQLite
import sqlite3 as lite

# Criando a conexão
con = lite.connect('dados.db')

# Tabela Quantia Total
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Quantia(id INTEGER PRIMARY KEY AUTOINCREMENT, valor DECIMAL)")

# Tabela de Despesas
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Despesas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, descricao TEXT, valor DECIMAL)")