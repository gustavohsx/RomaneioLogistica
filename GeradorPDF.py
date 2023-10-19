from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime


class GerarPDF():

    def __init__(self, local_salvamento):
        self.pdf = canvas.Canvas(f'{local_salvamento.replace(".pdf", "")}.pdf', pagesize=A4)
        self.pdf.setTitle('modelo')

    def cabecalhoPaginaInicial(self):
        self.pdf.setFont('Helvetica-Bold', 18)
        self.pdf.drawString(190, 795, 'SPESSOA DISTRIBUIDOR')

        self.pdf.setFont('Helvetica-Bold', 12)
        self.pdf.drawString(35, 770, 'DE:')

        self.pdf.setFont('Helvetica', 12)
        self.pdf.drawString(35, 750, 'Motorista:')
        self.pdf.line(90, 750, 270, 750)
        self.pdf.drawString(35, 730, 'Placa:')
        self.pdf.line(70, 730, 270, 730)

        self.pdf.setFont('Helvetica-Bold', 12)
        self.pdf.drawString(300, 770, 'PARA:')

        self.pdf.setFont('Helvetica', 12)
        self.pdf.drawString(300, 750, 'Motorista:')
        self.pdf.line(355, 750, 535, 750)
        self.pdf.drawString(300, 730, 'Placa:')
        self.pdf.line(335, 730, 535, 730)

        self.pdf.drawString(35, 700, 'Nome Conferente:')
        self.pdf.line(135, 700, 335, 700)
        self.pdf.drawString(35, 680, 'Quant. Paletes:')
        self.pdf.line(120, 680, 210, 680)
        self.pdf.drawString(225, 680, 'Box:')
        self.pdf.line(250, 680, 335, 680)
        self.pdf.drawString(345, 700, 'Hora Inicio:')
        self.pdf.line(407, 700, 535, 700)
        self.pdf.drawString(345, 680, 'Hora Fim:')
        self.pdf.line(398, 680, 535, 680)



    def cabecalhoTabela(self, y):
        self.pdf.setFont('Helvetica-Bold', 11)
        self.pdf.drawString(30, y, 'Cod.Fábrica')
        self.pdf.drawString(200, y, 'Descrição')
        self.pdf.drawString(420, y, 'Cod.Barra')
        self.pdf.drawString(495, y, 'Qt')
        self.pdf.drawString(520, y, 'Unid.')
    
    def gerarQuadradoCheck(self, x, y):
        # linha de cima
        self.pdf.line(x[4]+20, y-5, x[4]+33, y-5)
        # linha de baixo
        self.pdf.line(x[4]+20, y+7, x[4]+33, y+7)
        # linha esquerda
        self.pdf.line(x[4]+20, y-5, x[4]+20, y+7)
        # linha direita
        self.pdf.line(x[4]+33, y-5, x[4]+33, y+7)
    
    def adicionarNotasFiscais(self, notas_fiscais):
        x = 60
        y = 652
        # 12 por linha
        for i in range(len(notas_fiscais)):
            if i == 14 or i == 28 or i == 42 or i == 56:
                x = 60
                y = y - 10
            self.pdf.setFont('Helvetica', 8)
            self.pdf.drawString(x, y, f'{notas_fiscais[i]}')
            if i != len(notas_fiscais)-1:
                self.pdf.drawString(x+30, y, f'-')
            x += 35
        
    def adicionarHora(self):
        data_e_hora_atuais = datetime.datetime.now()
        data_formatada = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S")
        self.pdf.drawString(30, 800, f'{data_formatada}')
    
    def adicionarImagemFundo(self):
        self.pdf.drawImage('logo_fundo.png', 35, 200, 500, 400)

    def informacoesUltimaPagina(self, y, peso_bruto, peso_liquido, quantidade_total, quantidade_sku):
        self.pdf.setFont('Helvetica-Bold', 10)
        self.pdf.drawString(35, y-10, f'Peso Bruto:')
        self.pdf.setFont('Helvetica', 10)
        self.pdf.drawString(100, y-10, f'{peso_bruto:.3f} kg')
        self.pdf.setFont('Helvetica-Bold', 10)
        self.pdf.drawString(200, y-10, f'Peso Liquido:')
        self.pdf.setFont('Helvetica', 10)
        self.pdf.drawString(270, y-10, f'{peso_liquido:.3f} kg')
        self.pdf.setFont('Helvetica-Bold', 10)
        self.pdf.drawString(360, y-10, f'{int(quantidade_sku)} produtos listados')
        self.pdf.drawString(490, y-10, f'{int(quantidade_total)} itens')

    def adicionarProdutosPaginaInicial(self, produtos, notas_fiscais=0, numero_pagina=1, peso_bruto=0, peso_liquido=0, quantidade_total=0, quantidade_sku=0, ultima_pagina=False, quant_paginas=1):
        self.pdf.setFont('Helvetica-Bold', 10)
        self.adicionarHora()
        self.pdf.drawString(500, 800, f'Página {numero_pagina} de {quant_paginas}')
        
        self.pdf.drawString(30, 652, 'NFs:')
        self.adicionarNotasFiscais(notas_fiscais)
        self.adicionarImagemFundo()
        x = [35, 100, 410, 510, 520]
        y = 580
        self.pdf.line(30, 590, 555, 590)
        for produto in produtos:
            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawString(x[0], y, produto.codigo_fabrica[5:])
            if len(produto.descricao) <= 54:
                self.pdf.drawString(x[1], y, produto.descricao)
            elif len(produto.descricao) <= 56:
                self.pdf.setFont('Helvetica', 9) 
                self.pdf.drawString(x[1], y+2, produto.descricao)
            else:
                self.pdf.setFont('Helvetica', 8) 
                self.pdf.drawString(x[1], y+3, produto.descricao[:60])
                self.pdf.drawString(x[1], y-7, produto.descricao[60:])
            self.pdf.setFont('Helvetica', 9)
            self.pdf.drawString(x[2], y, produto.codigo_barras)
            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawRightString(x[3], y, f'{int(produto.quantidade)}')
            self.pdf.drawString(x[4], y, produto.unidade)
            self.gerarQuadradoCheck(x, y)

            self.pdf.line(30, y-10, 555, y-10)

            y -= 20

        self.pdf.line(30, 590, 30, y+10)
        self.pdf.line(555, 590, 555, y+10)

        if ultima_pagina:
            self.informacoesUltimaPagina(y, peso_bruto, peso_liquido, quantidade_total, quantidade_sku)
    
    def adicionaProdutosPaginas(self, produtos, notas_fiscais=0, numero_pagina=2, peso_bruto=0, peso_liquido=0, quantidade_total=0, quantidade_sku=0, ultima_pagina=False, quant_paginas=1):
        self.pdf.setFont('Helvetica-Bold', 10)
        self.adicionarHora()
        self.pdf.drawString(500, 800, f'Página {numero_pagina} de {quant_paginas}')
        self.adicionarImagemFundo()
        x = [35, 100, 410, 510, 520]
        y = 740
        self.pdf.line(30, 750, 555, 750)
        for produto in produtos:
            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawString(x[0], y, produto.codigo_fabrica[5:])
            if len(produto.descricao) <= 54:
                self.pdf.drawString(x[1], y, produto.descricao)
            elif len(produto.descricao) <= 56:
                self.pdf.setFont('Helvetica', 9) 
                self.pdf.drawString(x[1], y+2, produto.descricao)
            else:
                self.pdf.setFont('Helvetica', 8) 
                self.pdf.drawString(x[1], y+3, produto.descricao[:60])
                self.pdf.drawString(x[1], y-7, produto.descricao[60:])

            self.pdf.setFont('Helvetica', 9)
            self.pdf.drawString(x[2], y, produto.codigo_barras)
            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawRightString(x[3], y, f'{int(produto.quantidade)}')
            self.pdf.drawString(x[4], y, produto.unidade)
            self.gerarQuadradoCheck(x, y)
            
            self.pdf.line(30, y-10, 555, y-10)

            y -= 20

        self.pdf.line(30, 750, 30, y+10)
        self.pdf.line(555, 750, 555, y+10)

        if ultima_pagina:
            self.informacoesUltimaPagina(y, peso_bruto, peso_liquido, quantidade_total, quantidade_sku)
    
    def paginaInicial(self, produtos, notas_fiscais=0, peso_bruto=0, peso_liquido=0, quantidade_total=0, quantidade_sku=0, ultima_pagina=False, quant_paginas=1, numero_pagina=1):
        self.cabecalhoPaginaInicial()
        self.cabecalhoTabela(y=600)
        self.adicionarProdutosPaginaInicial(produtos=produtos, notas_fiscais=notas_fiscais, numero_pagina=numero_pagina, peso_bruto=peso_bruto, peso_liquido=peso_liquido, quantidade_total=quantidade_total, quantidade_sku=quantidade_sku, ultima_pagina=ultima_pagina, quant_paginas=quant_paginas)

    def geraPDF(self, produtos, notas_fiscais=0, peso_bruto=0, peso_liquido=0, quantidade_total=0, quantidade_sku=0):
        quant_paginas = (len(produtos)//35) + 1
        quant_inicial = 0
        quant_final = 27
        if quant_paginas == 1:
            self.paginaInicial(produtos=produtos[quant_inicial:quant_final], notas_fiscais=notas_fiscais, numero_pagina=1, peso_bruto=peso_bruto, peso_liquido=peso_liquido, quantidade_total=quantidade_total, quantidade_sku=quantidade_sku, ultima_pagina=True, quant_paginas=quant_paginas)
        else:
            self.paginaInicial(produtos=produtos[quant_inicial:quant_final], notas_fiscais=notas_fiscais, numero_pagina=1, peso_bruto=peso_bruto, peso_liquido=peso_liquido, quantidade_total=quantidade_total, quantidade_sku=quantidade_sku, quant_paginas=quant_paginas)
            for i in range(2, quant_paginas+1):
                self.pdf.showPage()
                if i == quant_paginas:
                    quant_inicial = quant_final
                    quant_final += 35
                    self.cabecalhoTabela(y=760)
                    self.adicionaProdutosPaginas(produtos=produtos[quant_inicial:quant_final], notas_fiscais=notas_fiscais, numero_pagina=i, peso_bruto=peso_bruto, peso_liquido=peso_liquido, quantidade_total=quantidade_total, quantidade_sku=quantidade_sku, ultima_pagina=True, quant_paginas=quant_paginas)
                else:
                    quant_inicial = quant_final
                    quant_final += 35
                    self.cabecalhoTabela(y=760)
                    self.adicionaProdutosPaginas(produtos=produtos[quant_inicial:quant_final], notas_fiscais=notas_fiscais, numero_pagina=i, quant_paginas=quant_paginas)
        self.salvar()

    def salvar(self):
        self.pdf.save()