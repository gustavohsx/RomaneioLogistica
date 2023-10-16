import xml.etree.ElementTree as et
from tkinter import filedialog as fd
import DestinatarioDTO
import ProdutosDTO

class DadosXML:
    
    def __init__(self):
        self.dados = {}
    
    def selecionarArquivos(self):
        self.dados = {}
        caminhos_arquivos = fd.askopenfilenames(title='Selecionar arquivos', initialdir='./', filetypes=(('XML', '*.xml'), ('Todos os Arquivos', '*.*')))
        indice = 1
        for caminho in caminhos_arquivos:
            arquivo = et.parse(caminho)
            raiz = arquivo.getroot()
            self.raiz_inicial = raiz[0][0]
            self.dados[f'arquivo{indice}'] = self.obterDados()
            indice += 1

    def obterDados(self):
        cont_produtos = 0
        dados = {}
        for i in range(len(self.raiz_inicial)):
            aux = {}
            if self.raiz_inicial[i].tag.split("}")[1] == 'det':
                cont_produtos += 1
            for j in range(len(self.raiz_inicial[i])):
                aux2 = {}
                if len(self.raiz_inicial[i][j]) > 1:
                    try:
                        for k in range(len(self.raiz_inicial[i][j])):
                            aux2[f'{self.raiz_inicial[i][j][k].tag.split("}")[1]}'] = self.raiz_inicial[i][j][k].text if self.raiz_inicial[i][j][k] != None else f'{self.raiz_inicial[i][j][k].tag.split("}")[1]}'
                    except:
                        print('Entrou exceção')
                    aux[f'{self.raiz_inicial[i][j].tag.split("}")[1]}'] = aux2
                else:
                    aux2[f'{self.raiz_inicial[i][j].tag.split("}")[1]}'] = self.raiz_inicial[i][j].text if self.raiz_inicial[i][j] != None else f'{self.raiz_inicial[i][j].tag.split("}")[1]}'
                    aux[f'{self.raiz_inicial[i][j].tag.split("}")[1]}'] = self.raiz_inicial[i][j].text if self.raiz_inicial[i][j] != None else f'{self.raiz_inicial[i][j].tag.split("}")[1]}'
                
            if self.raiz_inicial[i].attrib.get("nItem") != None:
                dados[f'{self.raiz_inicial[i].tag.split("}")[1]}{self.raiz_inicial[i].attrib.get("nItem")}'] = aux
            else:
                dados[f'{self.raiz_inicial[i].tag.split("}")[1]}'] = aux
        dados['quantidade_produtos'] = cont_produtos
        return dados
    
    def __dadosProduto(self, arquivo, i):
        codigo_fabrica = arquivo[f'det{i}']['prod']['cProd']
        descricao = arquivo[f'det{i}']['prod']['xProd']
        unidade = arquivo[f'det{i}']['prod']['uCom']
        quantidade = float(arquivo[f'det{i}']['prod']['qCom'])
        codigo_barras = arquivo[f'det{i}']['prod']['cEAN']
        produto = ProdutosDTO.ProdutosDTO(codigo_fabrica, descricao, unidade, quantidade, codigo_barras)
        return produto

    def dadosDestinatario(self, arquivo):
        cnpj = arquivo['dest']['CNPJ']
        nome = arquivo['dest']['xNome']
        longradouro = arquivo['dest']['enderDest']['xLgr']
        numero = arquivo['dest']['enderDest']['nro']
        bairro = arquivo['dest']['enderDest']['xBairro']
        municipio = arquivo['dest']['enderDest']['xMun']
        uf = arquivo['dest']['enderDest']['UF']
        cep = arquivo['dest']['enderDest']['CEP']
        pais = arquivo['dest']['enderDest']['xPais']

        destinatario = DestinatarioDTO.DestinatarioDTO(nome, cnpj, longradouro, numero, bairro, municipio, uf, cep, pais)
        
        for i in range(1, arquivo['quantidade_produtos']+1):
            destinatario.adicionarProdutos(self.__dadosProduto(arquivo, i))
        return destinatario
    
# dados = DadosXML()
# dados.selecionarArquivos()
# for arquivo in dados.dados:
#     destinatario = dados.dadosDestinatario(dados.dados[arquivo])
#     print(destinatario.nome)
#     print(destinatario.cnpj)
#     print(len(destinatario.produtos))
#     for i in range(len(destinatario.produtos)):
#         print(destinatario.produtos[i])

            