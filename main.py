# importando componentes
from tkinter import Tk
from tkinter import StringVar
from tkinter import ttk
from tkinter import messagebox
from tkinter import Frame
from tkinter import Label
from PIL import Image
from PIL import ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

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

janela = Tk()
janela.title("")
janela.geometry('820x610')
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

app_img = Image.open('airplane3.png')
app_img = app_img.resize((45,45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameTopo, image=app_img, width=900, compound='left', padx=5, anchor='nw', bg=co0, fg=co13)
app_logo.place(x=320, y=-4)

# Editando o frame esquerdo dentro do frame central

def Totais():
    l_nome = Label(frame_esquerda, text="Orçamentos e despesas", width=30, height=1, anchor='nw', font=('Source Code Pro', 11), bg=co14, fg=co0)
    l_nome.place(x=0, y=0)
    
    # Orçamento Total

    l_total_orcamento = Label(frame_esquerda, text='Orçamento Total', anchor='nw', font=('Source Code Pro', 10), bg=co16, fg=co0)
    l_total_orcamento.place(x=10, y=50)

    valor_total = 10000

    l_orcamento = Label(frame_esquerda, text='${:,.2f}'.format(valor_total), width=25, anchor='nw', font=('Input', 12), bg=co1, fg=co4)
    l_orcamento.place(x=10, y=80)

    # Despesas Totais

    l_total_despesa = Label(frame_esquerda, text='Despesas Totais', anchor='nw', font=('Source Code Pro', 10), bg=co15, fg=co0)
    l_total_despesa.place(x=10, y=120)

    valor_despesa = 10000

    l_despesa = Label(frame_esquerda, text='${:,.2f}'.format(valor_despesa), width=25, anchor='nw', font=('Input', 12), bg=co1, fg=co4)
    l_despesa.place(x=10, y=150)

    # Valores Restantes

    l_total_restante = Label(frame_esquerda, text='Valores Restantes', anchor='nw', font=('Source Code Pro', 10), bg=co0, fg=co1)
    l_total_restante.place(x=10, y=190)

    valor_restante = 10000

    l_restante = Label(frame_esquerda, text='${:,.2f}'.format(valor_restante), width=25, anchor='nw', font=('Input', 12), bg=co1, fg=co4)
    l_restante.place(x=10, y=220)

def grafico_pie():
    
    figura = plt.Figure(figsize=(7, 4), dpi=87)
    ax = figura.add_subplot(111)

    lista_valores = [56,78,45,92]
    lista_categorias = ['alimentacao', 'transporte', 'Acomodacao', 'Entretenimento']

    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90, textprops={'color': 'white'})

    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    figura.set_facecolor('#666666')

    frame_direita_pie = Frame(frame_direita, width=600, height=290, bg=co0, pady=0, relief="raised")
    frame_direita_pie.place(x=-60, y=-25)
    l_nome = Label(frame_direita, text="Como estão distribuídas as minhas despesas?", width=60, height=1, anchor='center', padx=2, font=('Verdana', 11), bg=co14, fg=co0)
    l_nome.place(x=0, y=1)
    
    canva_categoria = FigureCanvasTkAgg(figura, frame_direita_pie)
    canva_categoria.get_tk_widget().grid(row=0,column=0,padx=0)

# grafico
def grafico():
    global frame_tabela
    l_nome = Label(frameBaixo, text="Quais são as minhas despesas?", width=87, height=1, anchor='nw', padx=10, font=('Source Code Pro', 11), bg=co14, fg=co0)    
    l_nome.grid(row=0, column=0, columnspan=6, pady=0, padx=0)

    frame_tabela = Frame(frameBaixo, width=330, height=250, bg=co12)
    frame_tabela.grid(row=1, column=0, pady=0, padx=3)

    frame_operacoes = Frame(frameBaixo, width=220, height=250, bg=co12)
    frame_operacoes.grid(row=1, column=1, pady=0, padx=3)

    frame_configuracao = Frame(frameBaixo, width=235, height=250, bg=co12)
    frame_configuracao.grid(row=1, column=2, pady=0, padx=3)

grafico()
# funcao para atribuir dados a tabela
def preencher_tabela():

    tabela_head = ['id', 'tipo', 'descrição', 'total']

    lista_itens = ['1','ddd','dddddd','122'], ['1','ddd','dddddd','122']

    global frame_tabela, tree

    tree = ttk.Treeview(frame_tabela, selectmode="extended", columns=tabela_head, show="headings")
    tree.grid(column=0, row=0, sticky='nsew')
    # Frame adicional para conter a barra de rolagem vertical
    frame_vsb = Frame(frame_tabela, bg=co0)
    frame_vsb.grid(column=1, row=0, sticky='ns')
    # barra de rolagem lateral
    vsb = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
    vsb.grid(column=1, row=0, sticky='ns')
    # barra de rolagem horizontal
    hsb = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tree.xview)
    hsb.grid(column=0, row=1, sticky='ew')

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    hd=["nw","nw","center","e","e"]
    h=[20, 90, 120, 90, 70]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor='center')
        tree.column(col, width=h[n], anchor=hd[n])

        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)


grafico_pie()
preencher_tabela()
Totais()

janela.mainloop()

