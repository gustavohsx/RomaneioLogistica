class ProdutosDTO:

    def __init__(self, codigo_fabrica, descricao, unidade, quantidade, codigo_barras):
        self.codigo_fabrica = codigo_fabrica
        self.descricao = descricao
        self.unidade = unidade
        self.quantidade = quantidade
        self.codigo_barras = codigo_barras
    
    def setQuantidade(self, quantidade):
        self.quantidade = quantidade

    def __str__(self) -> str:
        return f'{self.codigo_fabrica} - {self.descricao} - {self.quantidade}{self.unidade} - {self.codigo_barras}'
    