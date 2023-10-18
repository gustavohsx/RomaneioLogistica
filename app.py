import customtkinter
from tkinter import *
from tkinter import ttk, filedialog
import DadosXML
import GeradorPDF
import ProdutosDTO

    
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.tipo_filtragem_lista = ['Nota Fiscal', 'Cidade', 'Destinatario']
        self.dados = DadosXML.DadosXML()
        self.arquivos = []
        self.filtrados = {}
        self.impresso = False

        self.codigo_fabrica_produtos = []
        self.produtos = []
        self.peso_bruto = 0
        self.peso_liquido = 0
        self.notas_fiscais = []
        self.quantidade_total_produtos = 0
        self.produtos_pdf = None

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
        self.impresso = False
        self.filtrados = {}
        self.atualizarQuantidadeArquivos(len(self.dados.dados))
        self.obterDadosArquivos()
        self.ordenar(self.tipo_filtragem_combobox.get())
    
    def obterDadosArquivos(self):
        self.arquivos = []
        for indice_arquivo in self.dados.dados:
            destinatario = self.dados.dadosArquivo(self.dados.dados[indice_arquivo])
            self.arquivos.append(destinatario)
    
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

    def sortPeloIndice(self, e):
        return e[1]
    
    def ordenar(self, tipo):
        print('-'*100)
        self.filtrados = {}
        self.quantidade_total_produtos = 0
        if tipo.upper() == 'NOTA FISCAL':
            for arquivo in self.arquivos:
                aux = []
                aux.append(arquivo)
                self.filtrados[arquivo.nota_fiscal] = aux.copy()
                for produto in arquivo.produtos:
                    self.quantidade_total_produtos += produto.getQuantidade()

        elif tipo.upper() == 'CIDADE':
            for arquivo in self.arquivos:
                aux = []
                aux.append(arquivo)
                try:
                    self.filtrados[arquivo.municipio] = self.filtrados[arquivo.municipio] + aux.copy()
                except:
                    self.filtrados[arquivo.municipio] = aux.copy()
                for produto in arquivo.produtos:
                    self.quantidade_total_produtos += produto.getQuantidade()

        elif tipo.upper() == 'DESTINATARIO':
            for arquivo in self.arquivos:
                aux = []
                aux.append(arquivo)
                try:
                    self.filtrados[arquivo.nome] = self.filtrados[arquivo.nome] + aux.copy()
                except:
                    self.filtrados[arquivo.nome] = aux.copy()
                for produto in arquivo.produtos:
                    self.quantidade_total_produtos += produto.getQuantidade()

        print(self.filtrados.keys())
        self.adicionarProdutosTreeviewProdutos()
    
    def adicionarProdutosTreeviewProdutos(self):
        try:
            self.produtos_tabview.destroy()
        except Exception as e:
            print('Nao deu para apagar', e)
        self.produtos_tabview = customtkinter.CTkTabview(master=self)
        primeira_tab = ''
        for key in self.filtrados.keys():
            try:
                self.produtos_tabview.add(f'{key}')
                primeira_tab = f'{key}' if primeira_tab == '' else primeira_tab
            except Exception as e:
                print('Não deu para criar!', e)
            dados_produtos = []
            for destinatario in self.filtrados[key]:
                # print(destinatario)
                for produto in destinatario.produtos:
                    dados = (produto.codigo_fabrica, produto.descricao, f'{produto.quantidade} {produto.unidade}')
                    dados_produtos.append(dados)
            self.criarProdutosTreeview(master=self.produtos_tabview.tab(f'{key}'))
            dados_ordenados = sorted(dados_produtos, key=self.sortPeloIndice)
            for produto in dados_ordenados:
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
            self.arquivos.pop(self.arquivos.index(self.filtrados[aba_excluir][0]))
            self.filtrados.pop(aba_excluir)
            print('apagado')
        except Exception as e:
            print(e)

        self.impresso = False
        self.ordenar(self.tipo_filtragem_combobox.get())
    
    def gerarPDF(self):
        if not self.impresso:
            todos_produtos = {}
            self.peso_bruto = 0
            self.peso_liquido = 0
            self.notas_fiscais = []
            self.produtos = []
            for key in self.filtrados.keys():
                for arquivo in self.filtrados[key]:
                    self.notas_fiscais.append(arquivo.nota_fiscal)
                    self.peso_bruto += float(arquivo.peso_bruto)
                    self.peso_liquido += float(arquivo.peso_liquido)
                    for produto in arquivo.produtos:
                        try:
                            quantidade = todos_produtos[produto.codigo_fabrica].quantidade + produto.quantidade
                            produto_novo = ProdutosDTO.ProdutosDTO(produto.getCodigoFabrica(), produto.getDescricao(), produto.getUnidade(), quantidade, produto.getCodigoBarras())
                            todos_produtos[produto.codigo_fabrica] = produto_novo
                            # print('atualizando', produto_novo.getCodigoFabrica())
                        except:
                            todos_produtos[produto.codigo_fabrica] = produto
                            # print('inserindo agora', todos_produtos[produto.codigo_fabrica].getCodigoFabrica())
            # print(todos_produtos)
            for key in todos_produtos.keys():
                self.produtos.append(todos_produtos[key])
            # print('-'*40)
            # print(self.produtos)
        self.produtos_pdf = sorted(self.produtos, key=lambda x: x.descricao)
        print(self.produtos_pdf)
        print(len(self.produtos_pdf))
        print(self.quantidade_total_produtos)
        caminho = filedialog.asksaveasfilename(filetypes=(('PDF', '*.pdf'), ('Todos os Arquivos', '*.*')))
        pdf = GeradorPDF.GerarPDF(caminho)
        pdf.geraPDF(produtos=self.produtos_pdf, notas_fiscais=self.notas_fiscais, peso_bruto=self.peso_bruto, peso_liquido=self.peso_liquido, quantidade_total=self.quantidade_total_produtos)
        self.impresso = True

app = App()
app.mainloop()