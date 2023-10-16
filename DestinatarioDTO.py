class DestinatarioDTO:

    def __init__(self, nome, cnpj, longradouro, numero, bairro, municipio, uf, cep, pais):
        self.nome = nome
        self.cnpj = cnpj
        self.longradouro = longradouro
        self.numero = numero
        self.bairro = bairro
        self.municipio = municipio
        self.uf = uf
        self.cep = cep
        self.pais = pais
        self.produtos = []
    
    def adicionarProdutos(self, produto):
        self.produtos.append(produto)
    
    def __str__(self) -> str:
        return f'{self.nome} - {self.cnpj}'