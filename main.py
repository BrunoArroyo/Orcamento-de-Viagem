# importando componentes
from tkinter import Tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import messagebox
from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from view import obter_valor_total
from view import atualizar_quantia_total
from view import inserir_despesa
from view import visualizar_quantia_despesas
from view import visualizar_quantia
from view import apagar_linha_despesa
from view import limpar_tabela_despesas
from view import dados_tabela_despesas
from view import exportar_planilha
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import os

# cores

co0 = "#2e2d2b"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"  # letra
co5 = "#e06636"  # - profit
co6 = "#038cfc"  # azul
co7 = "#3fbfb9"  # verde
co8 = "#263238"  # + verde
co9 = "#e9edf5"  # + verde
co10 = "#6e8faf"  # Azul Acinzentado
co11 = "#f2f4f2" # Cinza Claro Esverdeado
co12 = "#666666" # Cinza Médio Escuro
co13 = "#DDDDDD" # Cinza Claro
co14 = "#F5F5F5" # Cinza Muito Claro
co15 = "#FFC0CB" # Vermelho Claro
co16 = "#98FB98" # Verde Claro
colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']

# criando a tela principal

def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2

    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

janela = Tk()
janela.title("")
largura_janela = 820
altura_janela = 610
# Centralizar a janela
centralizar_janela(janela, largura_janela, altura_janela)
janela.configure(background=co1)
janela.resizable(width=False, height=False)

style = ttk.Style(janela)

# Frames

frameTopo = Frame(janela, width=1043, height=50, bg=co0)
frameTopo.grid(row=0, column=0)

frameCentral = Frame(janela, width=1043, height=290, bg=co0, padx=10)
frameCentral.grid(row=1, column=0)

frame_esquerda = Frame(frameCentral, width=255, height=290, bg=co12, pady=0, relief="raised")
frame_esquerda.place(x=-10, y=5)

frame_direita = Frame(frameCentral, width=630, height=290, bg=co0, pady=0, relief="raised")
frame_direita.place(x=250, y=5)

frameBaixo = Frame(janela, width=840, height=300, bg=co0)
frameBaixo.grid(row=2, column=0, pady=0, padx=0, sticky='NESW')

# Colocando a Logo

app_ = Label(frameTopo, text="Orçamento de Viagem", compound='left', padx=5, anchor='nw', font=('Source Code Pro', 20), bg=co0, fg=co13)
app_.place(x=0, y=0)

# Inserindo a imagem

app_img = Image.open('img/airplane3.png')
app_img = app_img.resize((45,45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameTopo, image=app_img, width=900, compound='left', padx=5, anchor='nw', bg=co0, fg=co13)
app_logo.place(x=320, y=-4)

# Editando o frame esquerdo dentro do frame central

def Totais():
    global valor_total, l_orcamento, valor_despesa
    l_nome = Label(frame_esquerda, text="Orçamentos e despesas", width=30, height=1, anchor='nw', font=('Source Code Pro', 11), bg=co14, fg=co0)
    l_nome.place(x=0, y=0)
    
    # Orçamento Total

    l_total_orcamento = Label(frame_esquerda, text='Orçamento Total', anchor='nw', font=('Source Code Pro', 10), bg=co16, fg=co0)
    l_total_orcamento.place(x=10, y=50)

    valor_total = obter_valor_total()

    l_orcamento = Label(frame_esquerda, text='${:,.2f}'.format(valor_total), width=25, anchor='nw', font=('Input', 12), bg=co1, fg=co4)
    l_orcamento.place(x=10, y=80)

    # Despesas Totais

    l_total_despesa = Label(frame_esquerda, text='Despesas Totais', anchor='nw', font=('Source Code Pro', 10), bg=co15, fg=co0)
    l_total_despesa.place(x=10, y=120)

    valor_despesa = visualizar_quantia_despesas()

    l_despesa = Label(frame_esquerda, text='${:,.2f}'.format(valor_despesa), width=25, anchor='nw', font=('Input', 12), bg=co1, fg=co4)
    l_despesa.place(x=10, y=150)

    # Valores Restantes

    l_total_restante = Label(frame_esquerda, text='Valores Restantes', anchor='nw', font=('Source Code Pro', 10), bg=co0, fg=co1)
    l_total_restante.place(x=10, y=190)

    valor_restante = valor_total - valor_despesa

    l_restante = Label(frame_esquerda, text='${:,.2f}'.format(valor_restante), width=25, anchor='nw', font=('Input', 12), bg=co1, fg=co4)
    l_restante.place(x=10, y=220)

    valor_quantia = visualizar_quantia()
    despesas = obter_despesas_do_bd()
    grafico_pie(valor_quantia, despesas)

def grafico_pie(valor_quantia, despesas):
    global figura
    figura = plt.Figure(figsize=(7, 4), dpi=87)
    ax = figura.add_subplot(111)

    # Calcular a soma total das despesas
    total_despesas = sum(despesa[3] for despesa in despesas)

    # Calcular a quantia restante
    quantia_restante = valor_quantia - total_despesas

    # Verificar se o valor total das despesas ultrapassou o orçamento
    if quantia_restante < 0:
        # Exibir uma mensagem de aviso
        messagebox.showwarning("Atenção", "O valor total das despesas ultrapassou o orçamento de viagem!")
        quantia_restante = 0  # Define quantia restante como 0 para evitar valores negativos no gráfico

    # Inicializar as listas de valores e categorias
    lista_valores = []
    lista_categorias = []

    # Adicionar a quantia restante ao gráfico (se for maior que 0)
    if quantia_restante > 0:
        lista_valores.append(quantia_restante)
        lista_categorias.append('Quantia Disponível')

    # Adicionar as despesas ao gráfico
    for despesa in despesas:
        descricao_despesa = despesa[2]  # Coluna 'descricao'
        valor_despesa = despesa[3]  # Coluna 'valor'
        lista_categorias.append(descricao_despesa)
        lista_valores.append(valor_despesa)

    # Explode para cada fatia do gráfico
    explode = [0.05] * len(lista_categorias)

    # Gerar gráfico de pizza
    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors, shadow=True, startangle=90, textprops={'color': 'white'})

    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    figura.set_facecolor('#666666')

    frame_direita_pie = Frame(frame_direita, width=600, height=290, bg=co0, pady=0, relief="raised")
    frame_direita_pie.place(x=-60, y=-25)
    l_nome = Label(frame_direita, text="Como estão distribuídas as minhas despesas?", width=60, height=1, anchor='center', padx=2, font=('Source Code Pro', 11), bg=co14, fg=co0)
    l_nome.place(x=0, y=1)

    canva_categoria = FigureCanvasTkAgg(figura, frame_direita_pie)
    canva_categoria.get_tk_widget().grid(row=0, column=0, padx=0)

    return figura

# abre tela de busca para achar um local e salva uma imagem do gráfico lá
def exportar_grafico():
    # Abrir uma janela de diálogo para salvar o arquivo
    file_path = filedialog.asksaveasfilename(
        defaultextension='.png', 
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
        title="Salvar gráfico"
    )
    
    # Se o caminho for válido (o usuário não cancelou)
    if file_path:
        try:
            figura.savefig(file_path)  # Exporta a figura para o caminho escolhido
            messagebox.showinfo("Sucesso", f"Gráfico exportado com sucesso para {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao exportar o gráfico: {str(e)}")

# grafico
def grafico():
    global frame_tabela, frame_operacoes, frame_configuracao
    l_nome = Label(frameBaixo, text="Quais são as minhas despesas?", width=87, height=1, anchor='nw', padx=10, font=('Source Code Pro', 11), bg=co14, fg=co0)    
    l_nome.grid(row=0, column=0, columnspan=6, pady=0, padx=0)

    frame_tabela = Frame(frameBaixo, width=330, height=250, bg=co12)
    frame_tabela.grid(row=1, column=0, pady=0, padx=3)

    frame_operacoes = Frame(frameBaixo, width=220, height=250, bg=co12)
    frame_operacoes.grid(row=1, column=1, pady=0, padx=3)

    frame_configuracao = Frame(frameBaixo, width=235, height=250, bg=co12)
    frame_configuracao.grid(row=1, column=2, pady=0, padx=3)

grafico()

# funcao para puxar os dados da tabela despesas

def obter_despesas_do_bd():
    con = sqlite3.connect('dados.db')
    cur = con.cursor()
    cur.execute("SELECT id, categoria, descricao, valor FROM Despesas")
    despesas = cur.fetchall()
    con.close()
    return despesas

# Configuracoes dos botões da Despesas

l_info = Label(frame_operacoes, text="Detalhes da despesa:", height=1, anchor='nw', font=('Source Code Pro', 10, 'bold'), bg=co1, fg=co4)
l_info.place(x=10, y=10)

l_categoria = Label(frame_operacoes, text='Categoria', anchor='nw', font=('Source Code Pro', 10), bg=co1, fg=co4)
l_categoria.place(x=10, y=40)

# Definindo as categorias

categorias = ['Transporte', 'Acomodação', 'Alimentação', 'Entretenimento', 'Seguro Viagem', 'Taxas', 'Outros']

combo_categoria_despesas = ttk.Combobox(frame_operacoes, width=12, font=('Source Code Pro', 10), state='readonly')
combo_categoria_despesas['values'] = (categorias)
combo_categoria_despesas.place(x=95, y=39)

l_descricao = Label(frame_operacoes, text="Descrição", anchor='nw', font=('Source Code Pro', 10), bg=co1, fg=co4)
l_descricao.place(x=10, y=70)
e_descricao = Entry(frame_operacoes, width=19, justify='left', relief='solid')
e_descricao.place(x=95, y=71)

l_valor_quantia = Label(frame_operacoes, text="Quantia", width=9, height=1, anchor='nw', font=('Source Code Pro', 10), bg=co1, fg=co4)
l_valor_quantia.place(x=10, y=100)
e_valor_despesa = Entry(frame_operacoes, width=19, justify='left', relief='solid')
e_valor_despesa.place(x=95, y=101)

# funcao para atribuir dados a tabela
def preencher_tabela():
    # Definir as colunas exibidas (sem a coluna 'id')
    tabela_head = ['tipo', 'descrição', 'total']

    lista_itens = obter_despesas_do_bd()

    global frame_tabela, tree

    # Criar a Treeview e adicionar a coluna oculta para o ID
    tree = ttk.Treeview(frame_tabela, selectmode="extended", columns=["id"] + tabela_head, show="headings")
    tree.grid(column=0, row=0, sticky='nsew')

    # Barra de rolagem lateral
    vsb = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
    vsb.grid(column=1, row=0, sticky='ns')

    # Barra de rolagem horizontal
    hsb = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tree.xview)
    hsb.grid(column=0, row=1, sticky='ew')

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Definir os formatos de cabeçalho (ID será oculto)
    hd = ["nw", "nw", "e"]
    h = [90, 120, 70]
    n = 0

    # Configurar os cabeçalhos e tamanhos das colunas
    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor='center')
        tree.column(col, width=h[n], anchor=hd[n])
        n += 1

    # Ocultar a coluna de ID
    tree.column("id", width=0, stretch=False)
    tree.heading("id", text="", anchor='center')

    # Preencher a tabela com as colunas 'categoria', 'descrição' e 'valor', e armazenar o 'id' de forma oculta
    for despesa in lista_itens:
        tree.insert('', 'end', values=(despesa[0], despesa[1], despesa[2], despesa[3]))

    # Atualizar gráfico
    valor_quantia = visualizar_quantia()
    despesas = obter_despesas_do_bd()
    grafico_pie(valor_quantia, despesas)

preencher_tabela()

# funcao para a tabela de despesas

def inserir_tabela_despesas():
    # Obtendo os valores dos widgets
        categoria = combo_categoria_despesas.get()
        descricao = e_descricao.get()
        valor = e_valor_despesa.get()
        
    # Verificando se todos os campos estão preenchidos
        try:
            categoria = str(categoria)
            descricao = str(descricao)
            valor = float(valor)
            i = [categoria, descricao, valor]
            if categoria and descricao and valor:
            # Conectando ao banco de dados
                inserir_despesa(i)
    
        except ValueError as e:
            mensagem_erro = f"Erro: {str(e)}"
            messagebox.showerror("Erro", mensagem_erro)
        
        # Limpando campos após interação
        combo_categoria_despesas.set('')
        e_descricao.delete(0, 'end')
        e_valor_despesa.delete(0, 'end')

        # Colocando valores na tabela
        preencher_tabela()

        # Atualizando Orçamentos e Despesas
        Totais()

# Colocando o botão inserir

img_add_despesas = Image.open('img/add.png')
img_add_despesas = img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)
botao_inserir_despesas = Button(frame_operacoes, command=inserir_tabela_despesas, image=img_add_despesas, compound='left', anchor='nw', text="Adicionar".upper(), width=195, overrelief='ridge', font=('Source Code Pro', 7, 'bold'), bg=co1, fg=co0)
botao_inserir_despesas.place(x=10, y=128)

# Colocando componente para atualizar o valor disponível

l_descricao2 = Label(frame_configuracao, text="Atualizar a quantia total", height=1, anchor='nw', font=('Source Code Pro', 10), bg=co1, fg=co4)
l_descricao2.place(x=10, y=10)

l_valor_quantia = Label(frame_configuracao, text="Quantia total", height=1, anchor='nw', font=('Source Code Pro', 10), bg=co1, fg=co4)
l_valor_quantia.place(x=10, y=40)
e_valor_quantia = Entry(frame_configuracao, width=15, justify='left', relief='solid')
e_valor_quantia.place(x=125, y=41)

# função para o botão

def obter_valor():
    valor_digitado = e_valor_quantia.get()
    try:
        valor_digitado = float(valor_digitado)
        atualizar_quantia_total([valor_digitado, 1])
        Totais()
    except ValueError as e:
        mensagem_erro = f"Erro: {str(e)}"
        messagebox.showerror("Erro", mensagem_erro)
    e_valor_quantia.delete(0, 'end')

# Colocando o botão atualizar

img_atualizar_quantia = Image.open('img/update.png')
img_atualizar_quantia = img_atualizar_quantia.resize((17,17))
img_atualizar_quantia = ImageTk.PhotoImage(img_atualizar_quantia)
botao_inserir_quantia = Button(frame_configuracao, command=obter_valor, image=img_atualizar_quantia, compound='left', anchor='nw', text="Atualizar".upper(), width=85, overrelief='ridge', font=('Source Code Pro', 7, 'bold'), bg=co1, fg=co0)
botao_inserir_quantia.place(x=125, y=70)

# Componente de exclusão

l_excluir = Label(frame_operacoes, text="Opções de Exclusão:", anchor='nw', font=('Source Code Pro', 8, 'bold'), bg=co1, fg=co4)
l_excluir.place(x=10, y=157)

# função para o botão de exclusão

def apagar_linha_selecionada():
    selected_item = tree.selection()

    if not selected_item:
        # Nenhuma linha selecionada, exibe uma mensagem de aviso
        mensagem_erro = "Erro: Nenhuma linha selecionada, favor selecionar uma linha da tabela e tentar novamente."
        messagebox.showerror("Erro", mensagem_erro)
        return  # Evita erro se nenhum item for selecionado
    
    # Obter o ID da despesa (valores[0] agora contém o ID oculto)
    id_selecionado = tree.item(selected_item)['values'][0]

    try:
        apagar_linha_despesa(id_selecionado)  # Apagar do banco de dados
        preencher_tabela()  # Atualizar a tabela
        Totais()  # Atualizar totais
    except ValueError as ve:
        erro = str(ve)
        print(erro)

# função para limpar lista
        
def limpar_lista():
    dados = dados_tabela_despesas()
    
    if not dados:  # Verifica se dados está vazio (uma lista vazia)
        mensagem_erro = "Erro: Não há nada na tabela para limpar"
        messagebox.showerror("Erro", mensagem_erro)
        return
    else:
        limpar_tabela_despesas()
        preencher_tabela()
        Totais()

# Colocando botões para exclusão

img_delete = Image.open('img/delete.png')
img_delete = img_delete.resize((20, 20))
img_delete = ImageTk.PhotoImage(img_delete)
botao_deletar = Button(frame_operacoes, command=apagar_linha_selecionada, image=img_delete, compound='left', anchor='nw', text='Deletar linha selecionada'.upper(), width=195, overrelief='ridge', font=('Source Code Pro', 7), bg=co1, fg=co0)
botao_deletar.place(x=10, y=183)

img_limpar = Image.open('img/vassoura.png')
img_limpar = img_limpar.resize((20, 20))
img_limpar = ImageTk.PhotoImage(img_limpar)
botao_limpar = Button(frame_operacoes, command=limpar_lista, image=img_limpar, compound='left', anchor='nw', text='Limpar lista'.upper(), width=195, overrelief='ridge', font=('Source Code Pro', 7), bg=co1, fg=co0)
botao_limpar.place(x=10, y=213)

# botão para exportar um excel

img_excel = Image.open('img/excel.png')
img_excel = img_excel.resize((30, 30))
img_excel = ImageTk.PhotoImage(img_excel)
botao_excel = Button(frame_configuracao, command=exportar_planilha, image=img_excel, compound='left', anchor='nw', text='Exportar despesas numa planilha'.upper(), width=195, height=30, overrelief='ridge', font=('Source Code Pro', 7), bg=co1, fg=co0)
botao_excel.place(x=10, y=163)

# botão para baixar gráfico

img_grafico = Image.open('img/grafico.png')
img_grafico = img_grafico.resize((30, 30))
img_grafico = ImageTk.PhotoImage(img_grafico)
botao_grafico = Button(frame_configuracao, command=exportar_grafico, image=img_grafico, compound='left', anchor='nw', text='Exportar imagem do gráfico'.upper(), width=195, height=30, overrelief='ridge', font=('Source Code Pro', 7), bg=co1, fg=co0)
botao_grafico.place(x=10, y=203)

valor_quantia = visualizar_quantia()
despesas = obter_despesas_do_bd()
figura = grafico_pie(valor_quantia, despesas)
Totais()

style.theme_use("classic")
style.configure("Treeview", highlihtthickness=0, bd=0, font=('Input', 9))

janela.mainloop()

