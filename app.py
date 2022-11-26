from tkinter import ttk
from tkinter import *
import sqlite3

class Produto:
    def __init__(self, root):
        self.janela = root
        self.janela.title("App Gestor de Produtos")
        self.janela.resizable(1,1) # Ativar a redimensionamento da janela. Para desativá-la: (0,0)
        self.janela.wm_iconbitmap('recursos/icon.ico')
        frame = LabelFrame(self.janela, text="Registar um novo produto", font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=20)
        # Label Nome
        self.etiqueta_nome = Label(frame, text="Nome: ", font=('Calibri', 13)) # Etiqueta de texto localizada no frame
        self.etiqueta_nome.grid(row=1, column=0)
        # Entry Nome
        self.nome = Entry(frame, font=('Calibri', 13))
        self.nome.focus()
        self.nome.grid(row=1, column=1)
        # Label Preço
        self.etiqueta_preço = Label(frame, text="Preço: ", font=('Calibri', 13)) # Etiqueta de texto localizada no frame
        self.etiqueta_preço.grid(row=2, column=0)
        # Entry Preço
        self.preço = Entry(frame, font=('Calibri', 13))
        self.preço.grid(row=2, column=1)
        # Botão Adicionar Produto
        s = ttk.Style()
        s.configure("my.TButton", font=('Calibri', 14, 'bold'))
        self.botao_adicionar = ttk.Button(frame, text="Guardar produto", command=self.add_produto, style="my.TButton")
        self.botao_adicionar.grid(row=3, columnspan=2, sticky= W + E)
        # Mensagem informativa para o utilizador
        self.mensagem = Label(text="", fg='red')
        self.mensagem.grid(row=3, column=0, columnspan=2, sticky= W +E)
        # Tabela de Produtos
        # Estilo personalizado para a tabela
        style = ttk.Style()
        style.configure("mystyle.Treeview",  highlightthickness=0, bd=0, font=("Calibri", 11))
        style.configure("mystyle.Treeviwe.Heading", font=("Calibri", 13, "bold"))
        style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky":"nswe"})]) # Eliminar as bordas
        # Estrutra das tabelas
        self.tabela = ttk.Treeview(height=20, columns = 2, style="mystyle.Treeview")
        self.tabela.grid(row=4, column=0, columnspan=2)
        self.tabela.heading("#0", text="Nome", anchor=CENTER)  # Cabeçalho 0
        self.tabela.heading("#1", text="Preço", anchor=CENTER)  # Cabeçalho 1
        # Botões eliminar e editar
        s = ttk.Style()
        s.configure("my.TButton", font=('Calibri', 14, 'bold'))
        botão_eliminar = ttk.Button(text="ELIMINAR", command=self.del_produto, style="my.TButton")
        botão_eliminar.grid(row=5, column=0, sticky= W + E)
        botão_editar = ttk.Button(text="EDITAR", command=self.edit_produto, style="my.TButton")
        botão_editar.grid(row=5, column=1, sticky= W + E)
        # Janela nova (editar produto)

        self.get_produtos()

    # Conection db
    db = "database/produtos.db"

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_produtos(self):
        # O primeiro, ao iniciar a app, vamos limpar a tabela se tiver dados residuais ou antigos
        registos_tabela = self.tabela.get_children()
        for linha in registos_tabela:
            self.tabela.delete(linha)
        # Consultar SQL
        query = 'SELECT * FROM produto ORDER BY nome DESC'
        registos_db = self.db_consulta(query)
        # Escrever os dados no ecrã
        for linha in registos_db:
            print(linha)
            self.tabela.insert("", 0, text=linha[1], values=linha[2])

    def validacao_nome(self):
        nome_introducido_por_utilizador = self.nome.get()
        return len(nome_introducido_por_utilizador) != 0

    def validacao_preco(self):
        preco_introducido_por_utilizador = self.preço.get()
        return len(preco_introducido_por_utilizador) != 0

    def add_produto(self):
        if self.validacao_nome() and self.validacao_preco():
            query = "INSERT INTO produto VALUES(NULL, ?, ?)"
            parametros = (self.nome.get(), self.preço.get())
            self.db_consulta(query, parametros)
            self.mensagem['text'] = "Produto '{}' adicionado com êxito".format(self.nome.get())
            self.nome.delete(0, END)
            self.preço.delete(0, END)

            # print(self.nome.get())
            # print(self.preço.get())
        elif self.validacao_nome() and self.validacao_preco() == False:
            print("O preço é obrigatórios")
            self.mensagem["text"] = "O preço é obrigatório"
        elif self.validacao_nome() == False and self.validacao_preco():
            print("O nome é obrigatórios")
            self.mensagem["text"] = "O nome é obrigatório"
        else:
            print("O nome e o preço são obrigatórios")
            self.mensagem["text"] = "O nome e o preço são obrigatórios"

        self.get_produtos()
        # Quando se finalizar a inserção de dados voltamos a invocar este método para atualizar o conteúdo e ver as alterações

    def del_produto(self):
        # print(self.tabela.item(self.tabela.selection()))
        # print(self.tabela.item(self.tabela.selection())["text"])
        # print(self.tabela.item(self.tabela.selection())["values"])
        # print(self.tabela.item(self.tabela.selection())["values"][0])

        self.mensagem["text"] = ""
        try:
            self.tabela.item(self.tabela.selection())["text"][0]
        except IndexError as e:
            self.mensagem["text"] = "Por favor, selecione um produto"
            return

        self.mensagem["text"] = ""
        nome = self.tabela.item(self.tabela.selection())["text"]
        query = "DELETE FROM produto WHERE nome = ?"
        self.db_consulta(query, (nome,))
        self.mensagem["text"] = "Produto '{}' eliminado com êxito".format(nome)
        self.get_produtos()

    def edit_produto(self):
        self.mensagem["text"] = ""
        try:
            self.tabela.item(self.tabela.selection())["text"][0]
        except IndexError as e:
            self.mensagem["text"] = "Por favor, selecione um produto"
            return

        nome = self.tabela.item(self.tabela.selection())["text"]
        old_preco = self.tabela.item(self.tabela.selection())['values'][0]

        self.janela_editar = Toplevel()
        self.janela_editar.title = "Editar Produto"
        self.janela_editar.resizable(1,1)
        self.janela_editar.wm_iconbitmap("recursos/icon.ico")

        titulo = Label(self.janela_editar, text="Edição de Produtos", font=("Calibri", 35, "bold"))
        titulo.grid(column=0, row=0)

        # Criação do recipiente Frame da janela de Editar Produto
        frame_ep = LabelFrame(self.janela_editar, text="Editar o seguinte Produto", font=('Calibri', 16, 'bold'))
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nome antigo
        self.etiqueta_nome_antigo = Label(frame_ep, text="Nome antigo: ", font=('Calibri', 13))
        self.etiqueta_nome_antigo.grid(row=2, column=0)
        # Entry Nome antigo (texto que não se poderá modificar)
        self.input_nome_antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=nome), state="readonly", font=('Calibri', 13))
        self.input_nome_antigo.grid(row=2, column=1)

        # Label Nome novo
        self.etiqueta_nome_novo = Label(frame_ep, text="Nome novo: ", font=('Calibri', 13))
        self.etiqueta_nome_novo.grid(row=3, column=0)
        # Entry Nome novo (texto que se poderá modificar)
        self.input_nome_novo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nome_novo.grid(row=3, column=1)
        self.input_nome_novo.focus()

        # Label Preço antigo
        self.etiqueta_preco_antigo = Label(frame_ep, text="Preço antigo: ", font=('Calibri', 13))
        self.etiqueta_preco_antigo.grid(row=4, column=0)
        # Entry preço antigo (Não se poderá modifcar)
        self.input_preco_antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=old_preco), state="readonly", font=('Calibri', 13))
        self.input_preco_antigo.grid(row=4, column=1)

        # Label preço novo
        self.etiqueta_preco_novo = Label(frame_ep, text="Preço novo: ", font=('Calibri', 13))
        self.etiqueta_preco_novo.grid(row=5, column=0)
        # Entry preço novo
        self.input_preco_novo = Entry(frame_ep, font=('Calibri', 13))
        self.input_preco_novo.grid(row=5, column=1)

        # Botão Atualizar produto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botão_atualizar = ttk.Button(frame_ep, text="Atualizar Produto", style='my.TButton',
                                          command=lambda:
        self.atualizar_produtos(self.input_nome_novo.get(),
                                self.input_nome_antigo.get(),
                                self.input_preco_novo.get(),
                                self.input_preco_antigo.get()
                                ))
        self.botão_atualizar.grid(row=6, columnspan=2, sticky= W + E)

    def atualizar_produtos(self, novo_nome, antigo_nome, novo_preco, antigo_preco):
        produto_modificado = False
        query = "UPDATE produto SET nome = ?, preço = ? WHERE nome = ? AND preço = ?"
        if novo_nome != '' and novo_preco != '':
            parametros = (novo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome != '' and novo_preco == '':
            parametros = (novo_nome, antigo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome == "" and novo_preco != "":
            parametros = (antigo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True

        if(produto_modificado):
            self.db_consulta(query, parametros)
            self.janela_editar.destroy() # Fechar a janela de edcição de produtos
            self.mensagem["text"] = "O produto '{}' foi atualizado com êxito".format(antigo_nome)
            self.get_produtos() # Atualizar a tabela de produtos
        else:
            self.janela_editar.destroy()
            self.mensagem["text"] = "O produto '{}' NÃO foi atualizado".format(antigo_nome)

if __name__ == "__main__":
    root = Tk() # Instância da janela principal
    app = Produto(root) # Envia-se para a classe Produto o controlo sobre a janela root
    root.mainloop()  # Começamos o ciclo de aplicação, é como um while True