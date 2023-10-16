import customtkinter
from tkinter import *
from tkinter import ttk
import DadosXML

    
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.tipo_filtragem_lista = ['Cidade', 'Bairro', 'Destinatario']
        self.dados = DadosXML.DadosXML()
        self.destinatarios = []
        self.filtrados = {}

        self.title("Romaneio Logistica")
        self.geometry("800x550")
        self.grid_columnconfigure((0, 1), weight=1)

        titulo_label = customtkinter.CTkLabel(self, text='Lista de Separação', font=(customtkinter.CTkFont(size=20)))
        inserir_arquivos_label = customtkinter.CTkLabel(self, text='Selecione os arquivos: ', font=(customtkinter.CTkFont(size=15)))
        inserir_arquivos_button = customtkinter.CTkButton(self, text='Selecionar Arquivos', font=(customtkinter.CTkFont(weight='bold')), command=self.selecionarArquivos)
        tipo_filtragem_label = customtkinter.CTkLabel(self, text='Selecione o Tipo de Filtragem: ', font=(customtkinter.CTkFont(size=15)))
        self.tipo_filtragem_combobox = customtkinter.CTkComboBox(self, values=self.tipo_filtragem_lista, command=self.ordenar)
        
        titulo_label.grid(column=0, row=0, columnspan=2, pady=30)
        inserir_arquivos_label.grid(column=0, row=1, sticky=E)
        inserir_arquivos_button.grid(column=1, row=1, sticky=W)
        tipo_filtragem_label.grid(column=0, row=3, sticky=E, pady=10)
        self.tipo_filtragem_combobox.grid(column=1, row=3, sticky=W)
        
        
    def selecionarArquivos(self):
        self.dados.selecionarArquivos()
        try:
            self.apagarQuantidadeArquivos()
        except Exception as e:
            print('Não foi possivel apagar a Label quantidade arquivos abertos!', e)
        self.atualizarQuantidadeArquivos(len(self.dados.dados))
        self.obterDadosArquivos()
        self.ordenar(self.tipo_filtragem_combobox.get())
    
    def obterDadosArquivos(self):
        self.destinatarios = []
        for indice_arquivo in self.dados.dados:
            destinatario = self.dados.dadosDestinatario(self.dados.dados[indice_arquivo])
            self.destinatarios.append(destinatario)
    
    def atualizarQuantidadeArquivos(self, quantidade):
        print(quantidade)
        self.quant_aquivos_carregados_label = customtkinter.CTkLabel(self, text=f'Foram carregados {quantidade} arquivos', )
        self.quant_aquivos_carregados_label.grid(column=1, row=2, sticky=W)
    
    def apagarQuantidadeArquivos(self):
        self.quant_aquivos_carregados_label.destroy()
    
    def criarProdutosTreeview(self, master):
        colunas_treeview = ('COD FABRICA', 'DESCRIÇÃO', 'QUANTIDADE')
        self.produtos_treeview = ttk.Treeview(master, columns=colunas_treeview, show='headings')
        self.produtos_treeview.heading('COD FABRICA', text='COD FABRICA')
        self.produtos_treeview.heading('DESCRIÇÃO', text='DESCRIÇÃO')
        self.produtos_treeview.heading('QUANTIDADE', text='QUANTIDADE')
        self.produtos_treeview.column('COD FABRICA', width=150, anchor=CENTER)
        self.produtos_treeview.column('DESCRIÇÃO', width=400, anchor=W)
        self.produtos_treeview.column('QUANTIDADE', width=100, anchor=CENTER)
        self.produtos_treeview.pack()
    
    def peloNome(self, e):
        return e.descricao
    
    def ordenar(self, tipo):
        self.filtrados = {}
        self.filtrados_produtos = {}
        if tipo.upper() == 'CIDADE':
            for destinatario in self.destinatarios:
                if destinatario.municipio.upper() not in self.filtrados.keys():
                    self.filtrados[destinatario.municipio.upper()] = []
                    self.filtrados[destinatario.municipio.upper()].append(destinatario)
                    self.filtrados_produtos[destinatario.municipio.upper()] = []
                    for produto in destinatario.produtos:
                        self.filtrados_produtos[destinatario.municipio.upper()].append(produto)
                else:
                    self.filtrados[destinatario.municipio.upper()].append(destinatario)
                    for produto in destinatario.produtos:
                        in_lista = False
                        for prod_lista in self.filtrados_produtos[destinatario.municipio.upper()]:
                            if produto.codigo_fabrica == prod_lista.codigo_fabrica:
                                print(produto, '-'*5, prod_lista)
                                quantidade = produto.quantidade + prod_lista.quantidade
                                produto.setQuantidade(quantidade)
                                prod_lista = produto
                                print(prod_lista)
                                in_lista= True
                        if not in_lista:
                            self.filtrados_produtos[destinatario.municipio.upper()].append(produto)
                    self.filtrados_produtos[destinatario.municipio.upper()].sort(key=self.peloNome)
        
        elif tipo.upper() == 'BAIRRO':
            for destinatario in self.destinatarios:
                if destinatario.bairro.upper() not in self.filtrados.keys():
                    self.filtrados[destinatario.bairro.upper()] = []
                    self.filtrados[destinatario.bairro.upper()].append(destinatario)
                    self.filtrados_produtos[destinatario.bairro.upper()] = []
                    for produto in destinatario.produtos:
                        self.filtrados_produtos[destinatario.bairro.upper()].append(produto)
                else:
                    self.filtrados[destinatario.bairro.upper()].append(destinatario)
                    for produto in destinatario.produtos:
                        in_lista = False
                        for prod_lista in self.filtrados_produtos[destinatario.bairro.upper()]:
                            if produto.codigo_fabrica == prod_lista.codigo_fabrica:
                                print(produto, '-'*5, prod_lista)
                                quantidade = produto.quantidade + prod_lista.quantidade
                                produto.setQuantidade(quantidade)
                                prod_lista = produto
                                print(prod_lista)
                                in_lista= True
                        if not in_lista:
                            self.filtrados_produtos[destinatario.bairro.upper()].append(produto)
                    self.filtrados_produtos[destinatario.bairro.upper()].sort(key=self.peloNome)

        elif tipo.upper() == 'DESTINATARIO':
            for destinatario in self.destinatarios:
                if destinatario.nome.upper() not in self.filtrados.keys():
                    self.filtrados[destinatario.nome.upper()] = []
                    self.filtrados[destinatario.nome.upper()].append(destinatario)
                    self.filtrados_produtos[destinatario.nome.upper()] = []
                    for produto in destinatario.produtos:
                        self.filtrados_produtos[destinatario.nome.upper()].append(produto)
                else:
                    self.filtrados[destinatario.nome.upper()].append(destinatario)
                    for produto in destinatario.produtos:
                        in_lista = False
                        for prod_lista in self.filtrados_produtos[destinatario.nome.upper()]:
                            if produto.codigo_fabrica == prod_lista.codigo_fabrica:
                                print(produto, '-'*5, prod_lista)
                                quantidade = produto.quantidade + prod_lista.quantidade
                                produto.setQuantidade(quantidade)
                                prod_lista = produto
                                print(prod_lista)
                                in_lista= True
                        if not in_lista:
                            self.filtrados_produtos[destinatario.nome.upper()].append(produto)
                    self.filtrados_produtos[destinatario.nome.upper()].sort(key=self.peloNome)
        
        self.adicionarProdutosTreeviewProdutos()

    def mostrarDadosFiltrados(self):
        self.imprimir = {}
        for key in self.filtrados.keys():
            #print(key, '-'*20)
            self.imprimir[key] = []
            for destinatario in self.filtrados[key]:
                #print(' '*4,destinatario.nome,destinatario.cnpj,destinatario.longradouro,destinatario.numero,destinatario.bairro,destinatario.municipio,destinatario.uf,destinatario.cep,destinatario.pais)
                for produto in destinatario.produtos:
                    #print(' '*8,produto.codigo_fabrica,produto.descricao,produto.unidade,produto.quantidade,produto.codigo_barras)
                    for i in range(len(self.imprimir[key])):
                        if produto.codigo_fabrica == self.imprimir[key][i].codigo_fabrica and produto.unidade == self.imprimir[key][i].unidade:
                            quantidade = produto.quantidade + self.imprimir[key][i].quantidade
                            produto.setQuantidade(quantidade)
                            print('achei')
                            self.imprimir[key].insert(i, produto)
                            self.imprimir[key].remove(self.imprimir[key][i+1])
                    self.imprimir[key].append(produto)
                #self.imprimir[key].sort()
            print(len(self.imprimir[key]))

    def apagarProdutosTabview(self):
        try:
            self.produtos_tabview.destroy()
        except Exception as e:
            print('Não foi possivel apagar a tabview!', e)
    
    # def adicionarProdutosTreeview(self):
    #     self.produtos_tabview = customtkinter.CTkTabview(master=self)
    #     primeira_tab = ''
    #     for key in self.filtrados.keys():
    #         try:
    #             self.produtos_tabview.add(f'{key}')
    #             primeira_tab = f'{key}' if primeira_tab == '' else primeira_tab
    #         except Exception as e:
    #             print('Não deu para criar!', e)
    #         dados_produtos = []
    #         for destinatario in self.filtrados[key]:
    #             for produto in destinatario.produtos:
    #                 dados = (produto.codigo_fabrica, produto.descricao, f'{produto.quantidade} {produto.unidade}')
    #                 dados_produtos.append(dados)
    #         self.criarProdutosTreeview(master=self.produtos_tabview.tab(f'{key}'))
    #         for produto in dados_produtos:
    #             self.produtos_treeview.insert('', END, values=produto)
    #         self.produtos_tabview.tab(f'{key}').grid()
    #     self.produtos_tabview.grid(column=0, row=4, columnspan=4)
    #     self.produtos_tabview.set(primeira_tab)

    #     botao = customtkinter.CTkButton(self, text='Clique', command=self.mostrarDadosFiltrados)
    #     botao.grid(column=0, row=6)
    
    def adicionarProdutosTreeviewProdutos(self):
        try:
            self.produtos_tabview.destroy()
        except Exception as e:
            print('Nao deu para apagar', e)
        self.produtos_tabview = customtkinter.CTkTabview(master=self)
        primeira_tab = ''
        for key in self.filtrados_produtos.keys():
            try:
                self.produtos_tabview.add(f'{key}')
                primeira_tab = f'{key}' if primeira_tab == '' else primeira_tab
            except Exception as e:
                print('Não deu para criar!', e)
            dados_produtos = []
            for produto in self.filtrados_produtos[key]:
                dados = (produto.codigo_fabrica, produto.descricao, f'{produto.quantidade} {produto.unidade}')
                dados_produtos.append(dados)
            self.criarProdutosTreeview(master=self.produtos_tabview.tab(f'{key}'))
            for produto in dados_produtos:
                self.produtos_treeview.insert('', END, values=produto)
            self.produtos_tabview.tab(f'{key}').grid()
        self.produtos_tabview.grid(column=0, row=4, columnspan=4)
        self.produtos_tabview.set(primeira_tab)

        botao = customtkinter.CTkButton(self, text='Clique', command=self.mostrarDadosFiltrados)
        botao.grid(column=0, row=6)

app = App()
app.mainloop()