# importando o SQLite
from tkinter import filedialog
import sqlite3 as lite
import tkinter as tk
import pandas as pd

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
    valor_quantia = 0  # Valor padrão caso não haja resultado

    with con:
        cur = con.cursor()
        cur.execute("SELECT valor FROM Quantia LIMIT 1")  # Pegar o primeiro (ou único) valor
        row = cur.fetchone()

        if row and isinstance(row[0], (int, float)):  # Certificar-se de que o valor é numérico
            valor_quantia = row[0]

    return valor_quantia


# Visualizar valor das despesas

def visualizar_quantia_despesas():
    total = 0

    with con:
        cur = con.cursor()
        cur.execute("SELECT VALOR FROM Despesas")
        rows = cur.fetchall()

        for row in rows:
            valor = row[0]  # Acesse o valor na posição 0 da tupla
            valor_formatado = float(valor)
            total += valor_formatado

    return total

# Atualizar quantidade

def atualizar_quantia_total(i):
    with con:
        cur = con.cursor()
        query = "UPDATE Quantia SET VALOR=? WHERE ID=?"
        cur.execute(query, i)

# Inserir Despesa

def inserir_despesa(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Despesas (categoria, descricao, valor) VALUES (?, ?, ?)"
        cur.execute(query, i)

# Apagar linha de despesas
        
def apagar_linha_despesa(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Despesas WHERE ID=?"
        cur.execute(query, (i,))

# Trazendo os dados da tabela de despesas
        
def dados_tabela_despesas():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Despesas")
        row = cur.fetchall()

        for i in row:
            lista_itens.append(i)
        
    return lista_itens

# Limpar tabela de despesas
        
def limpar_tabela_despesas():
    with con:
        cur = con.cursor()
        query = "DELETE FROM Despesas"
        cur.execute(query)



# Obter valor para aplicar na tela do sistema
def obter_valor_total():
    with con:
        cur = con.cursor()
        cur.execute("SELECT SUM(valor) FROM Quantia")
        resultado = cur.fetchone()
        return resultado[0] if resultado and resultado[0] is not None else 0.0

# abre tela para achar um local e salva uma planilha lá    
def exportar_planilha():
    dados = dados_tabela_despesas()

    if not dados:  # Verifica se dados está vazio (uma lista vazia)
        mensagem_erro = "Erro: Não há nada na tabela para exportar"
        messagebox.showerror("Erro", mensagem_erro)
        return
    else:
        dados_listados = [list(dado) for dado in dados]  # Adequando dados para exportação
        df = pd.DataFrame(dados_listados, columns=['ID', 'Categoria', 'Descrição', 'Valor'])  # Criando DataFrame

        # Adicionando uma nova coluna numerada antes da coluna 'Categoria'
        df.insert(1, 'Sequência', range(1, len(df) + 1))

        df_oficial = df.drop(columns=['ID'])  # Tirando coluna ID

        # Definindo o caminho do arquivo com um nome pré-definido "planilha"
        caminho_do_arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")], initialfile="planilha")

        if caminho_do_arquivo:
            df_oficial.to_excel(caminho_do_arquivo, index=False)


dados_tabela_despesas()