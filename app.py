import customtkinter
from tkinter import *
from tkinter import ttk
import DadosXML
import GeradorPDF

    
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.tipo_filtragem_lista = ['Nota Fiscal', 'Cidade', 'Destinatario']
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
            destinatario = self.dados.dadosArquivo(self.dados.dados[indice_arquivo])
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
    
    def sortPeloNome(self, e):
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
                                # print(produto, '-'*5, prod_lista)
                                quantidade = produto.quantidade + prod_lista.quantidade
                                produto.setQuantidade(quantidade)
                                prod_lista = produto
                                # print(prod_lista)
                                in_lista= True
                        if not in_lista:
                            self.filtrados_produtos[destinatario.municipio.upper()].append(produto)
                    self.filtrados_produtos[destinatario.municipio.upper()].sort(key=self.sortPeloNome)
        
        elif tipo.upper() == 'NOTA FISCAL':
            for destinatario in self.destinatarios:
                if destinatario.nota_fiscal.upper() not in self.filtrados.keys():
                    self.filtrados[destinatario.nota_fiscal.upper()] = []
                    self.filtrados[destinatario.nota_fiscal.upper()].append(destinatario)
                    self.filtrados_produtos[destinatario.nota_fiscal.upper()] = []
                    for produto in destinatario.produtos:
                        self.filtrados_produtos[destinatario.nota_fiscal.upper()].append(produto)
                else:
                    self.filtrados[destinatario.nota_fiscal.upper()].append(destinatario)
                    for produto in destinatario.produtos:
                        in_lista = False
                        for prod_lista in self.filtrados_produtos[destinatario.nota_fiscal.upper()]:
                            if produto.codigo_fabrica == prod_lista.codigo_fabrica:
                                # print(produto, '-'*5, prod_lista)
                                quantidade = produto.quantidade + prod_lista.quantidade
                                produto.setQuantidade(quantidade)
                                prod_lista = produto
                                # print(prod_lista)
                                in_lista= True
                        if not in_lista:
                            self.filtrados_produtos[destinatario.nota_fiscal.upper()].append(produto)
                    self.filtrados_produtos[destinatario.nota_fiscal.upper()].sort(key=self.sortPeloNome)

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
                                # print(produto, '-'*5, prod_lista)
                                quantidade = produto.quantidade + prod_lista.quantidade
                                produto.setQuantidade(quantidade)
                                prod_lista = produto
                                # print(prod_lista)
                                in_lista= True
                        if not in_lista:
                            self.filtrados_produtos[destinatario.nome.upper()].append(produto)
                    self.filtrados_produtos[destinatario.nome.upper()].sort(key=self.sortPeloNome)
        
        self.adicionarProdutosTreeviewProdutos()

    def mostrarDadosFiltrados(self):
        cont_filtrados = 0
        cont_filtrados_produtos = 0
        produtos = []
        for key in self.filtrados.keys():
            for destinatario in self.filtrados[key]:
                cont_filtrados += len(destinatario.produtos)
                for produto in destinatario.produtos:
                    produtos.append(produto.codigo_fabrica)
        
        for key in self.filtrados_produtos.keys():
            cont_filtrados_produtos += len(self.filtrados_produtos[key])
            for produto in self.filtrados_produtos[key]:
                print(produto.descricao, produto.quantidade,)
                print(produtos.count(produto.codigo_fabrica))

        print(cont_filtrados)
        print(cont_filtrados_produtos)

    def apagarProdutosTabview(self):
        try:
            self.produtos_tabview.destroy()
        except Exception as e:
            print('Não foi possivel apagar a tabview!', e)
    
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

        botao_excluir_aba_buttom = customtkinter.CTkButton(self, text='Excluir Aba', command=self.excluirAba)
        botao_excluir_aba_buttom.grid(column=0, row=6, stick=E, padx=15)

        botao_imprimir_produtos_buttom = customtkinter.CTkButton(self, text='Gerar PDF', command=self.gerarPDF)
        botao_imprimir_produtos_buttom.grid(column=1, row=6, sticky=W, padx=15)
    
    def excluirAba(self):
        aba_excluir = self.produtos_tabview.get()
        print(aba_excluir)
        self.produtos_tabview.delete(aba_excluir)
        try:
            self.filtrados_produtos.pop(aba_excluir)
            self.filtrados.pop(aba_excluir)
            print('apagado')
            print(self.filtrados_produtos.keys())
            print(self.filtrados.keys())
        except Exception as e:
            print(e)
    
    def gerarPDF(self):
        codigo_fabrica_produtos = []
        produtos = []
        peso_bruto = 0
        peso_liquido = 0
        for key in self.filtrados_produtos.keys():
            for produto in self.filtrados_produtos[key]:
                if produto.codigo_fabrica not in codigo_fabrica_produtos:
                    codigo_fabrica_produtos.append(produto.codigo_fabrica)
                    produtos.append(produto)
                    print('adicionado a lista produtos')
                else:
                    print('ja esta na lista produtos')
                    indice = codigo_fabrica_produtos.index(produto.codigo_fabrica)
                    print(produto.codigo_fabrica, produtos[indice].codigo_fabrica)
                    quantidade = produto.quantidade + produtos[indice].quantidade
                    produto.setQuantidade(quantidade)
                    produtos[indice] = produto
                    print(produtos[indice].codigo_fabrica)
            for arquivo in self.filtrados[key]:
                peso_bruto += float(arquivo.peso_bruto)
                peso_liquido += float(arquivo.peso_liquido)
        print(len(produtos))
        print(peso_bruto)
        print(peso_liquido)
        pdf = GeradorPDF
        pdf.adicionarProdutos(produtos)
        pdf.salvar()
        

app = App()
app.mainloop()