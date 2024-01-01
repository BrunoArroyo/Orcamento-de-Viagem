# importando componentes
from tkinter import Tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import ttk
from tkinter import messagebox
from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from PIL import Image
from PIL import ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from view import obter_valor_total
from view import atualizar_quantia_total
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
    global valor_total, l_orcamento
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
    l_nome = Label(frame_direita, text="Como estão distribuídas as minhas despesas?", width=60, height=1, anchor='center', padx=2, font=('Source Code Pro', 11), bg=co14, fg=co0)
    l_nome.place(x=0, y=1)
    
    canva_categoria = FigureCanvasTkAgg(figura, frame_direita_pie)
    canva_categoria.get_tk_widget().grid(row=0,column=0,padx=0)

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
# funcao para atribuir dados a tabela
def preencher_tabela():

    tabela_head = ['id', 'tipo', 'descrição', 'total']

    lista_itens = ['1','ddd','dddddd','122'], ['1','ddd','dddddd','122']

    global frame_tabela, tree

    tree = ttk.Treeview(frame_tabela, selectmode="extended", columns=tabela_head, show="headings")
    tree.grid(column=0, row=0, sticky='nsew')
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

preencher_tabela()

# Configuracoes dos botões da Despesas

l_info = Label(frame_operacoes, text="Inseria despesas abaixo:", height=1, anchor='nw', font=('Source Code Pro', 10, 'bold'), bg=co1, fg=co4)
l_info.place(x=10, y=10)

l_categoria = Label(frame_operacoes, text='Categoria', anchor='nw', font=('Source Code Pro', 10), bg=co1, fg=co4)
l_categoria.place(x=10, y=40)

# Definindo as categorias

categorias = ['Transporte', 'Arrendamento', 'Alimentacao', 'Entertainment', 'Outros']

combo_categoria_despesas = ttk.Combobox(frame_operacoes, width=12, font=('Source Code Pro', 10))
combo_categoria_despesas['values'] = (categorias)
combo_categoria_despesas.place(x=95, y=39)

l_descricao = Label(frame_operacoes, text="Descrição", anchor='nw', font=('Source Code Pro', 10), bg=co1, fg=co4)
l_descricao.place(x=10, y=70)
e_descricao = Entry(frame_operacoes, width=19, justify='left', relief='solid')
e_descricao.place(x=95, y=71)

l_valor_quantia = Label(frame_operacoes, text="Quantia", width=9, height=1, anchor='nw', font=('Source Code Pro', 10), bg=co1, fg=co4)
l_valor_quantia.place(x=10, y=120)
e_valor_despesa = Entry(frame_operacoes, width=19, justify='left', relief='solid')
e_valor_despesa.place(x=95, y=121)

# Colocando o botão inserir

img_add_despesas = Image.open('add.png')
img_add_despesas = img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)
botao_inserir_despesas = Button(frame_operacoes, command=preencher_tabela, image=img_add_despesas, compound='left', anchor='nw', text="Adicionar".upper(), width=100, overrelief='ridge', font=('Source Code Pro', 7, 'bold'), bg=co1, fg=co0)
botao_inserir_despesas.place(x=100, y=151)

# Colocando componente para atualizar o valor disponível

l_descricao2 = Label(frame_configuracao, text="Atualizar a quantia total", height=1, anchor='nw', font=('Source Code Pro', 10), bg=co1, fg=co4)
l_descricao2.place(x=10, y=10)

l_valor_quantia = Label(frame_configuracao, text="Quantia total", height=1, anchor='nw', font=('Source Code Pro', 10), bg=co1, fg=co4)
l_valor_quantia.place(x=10, y=40)
e_valor_quantia = Entry(frame_configuracao, width=15, justify='left', relief='solid')
e_valor_quantia.place(x=125, y=41)

def obter_valor():
    valor_digitado = e_valor_quantia.get()
    try:
        valor_digitado = float(valor_digitado)
        atualizar_quantia_total([valor_digitado, 1])
        Totais()
    except ValueError as e:
        mensagem_erro = f"Erro: {str(e)}"
        messagebox.showerror("Erro", mensagem_erro)

# Colocando o botão atualizar

img_atualizar_quantia = Image.open('update.png')
img_atualizar_quantia = img_atualizar_quantia.resize((17,17))
img_atualizar_quantia = ImageTk.PhotoImage(img_atualizar_quantia)
botao_inserir_quantia = Button(frame_configuracao, command=obter_valor, image=img_atualizar_quantia, compound='left', anchor='nw', text="Atualizar".upper(), width=85, overrelief='ridge', font=('Source Code Pro', 7, 'bold'), bg=co1, fg=co0)
botao_inserir_quantia.place(x=125, y=70)

# Componente de exclusão

l_excluir = Label(frame_configuracao, text="Excluir linha", anchor='nw', font=('Source Code Pro', 10, 'bold'), bg=co1, fg=co4)
l_excluir.place(x=10, y=120)

# Colocando botão para exclusão

img_delete = Image.open('delete.png')
img_delete = img_delete.resize((20, 20))
img_delete = ImageTk.PhotoImage(img_delete)
botao_deletar = Button(frame_configuracao, image=img_delete, compound='left', anchor='nw', text='Deletar'.upper(), width=85, overrelief='ridge', font=('Source Code Pro', 7), bg=co1, fg=co0)
botao_deletar.place(x=125, y=120)



grafico_pie()
Totais()

style.theme_use("classic")
style.configure("Treeview", highlihtthickness=0, bd=0, font=('Input', 9))

janela.mainloop()

