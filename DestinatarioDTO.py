class DestinatarioDTO:

    def __init__(self, nota_fiscal, nome, cnpj, longradouro, numero, bairro, municipio, uf, cep, pais, peso_bruto, peso_liquido):
        self.nota_fiscal = nota_fiscal
        self.nome = nome
        self.cnpj = cnpj
        self.longradouro = longradouro
        self.numero = numero
        self.bairro = bairro
        self.municipio = municipio
        self.uf = uf
        self.cep = cep
        self.pais = pais
        self.peso_bruto = peso_bruto
        self.peso_liquido = peso_liquido
        self.produtos = []
    
    def adicionarProdutos(self, produto):
        self.produtos.append(produto)
    
    def __str__(self) -> str:
        return f'{self.nome} - {self.cnpj}'