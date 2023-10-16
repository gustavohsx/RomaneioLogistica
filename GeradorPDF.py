from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


pdf = canvas.Canvas('modelo.pdf', pagesize=A4)
pdf.setTitle('modelo')

pdf.setFont('Helvetica-Bold', 18)
pdf.drawString(35, 770, 'SPESSOA DISTRIBUIDOR')

pdf.setFont('Helvetica-Bold', 12)
pdf.drawString(35, 750, 'DE:')

pdf.setFont('Helvetica', 12)
pdf.drawString(35, 730, 'Motorista:')
pdf.line(90, 730, 270, 730)
pdf.drawString(35, 710, 'Placa:')
pdf.line(70, 710, 270, 710)

pdf.setFont('Helvetica-Bold', 12)
pdf.drawString(300, 750, 'PARA:')

pdf.setFont('Helvetica', 12)
pdf.drawString(300, 730, 'Motorista:')
pdf.line(355, 730, 535, 730)
pdf.drawString(300, 710, 'Placa:')
pdf.line(335, 710, 535, 710)

# pdf.line(35, 680, 550, 680)
pdf.setFont('Helvetica-Bold', 12)
pdf.drawString(35, 660, 'COD FAB')
pdf.drawString(180, 660, 'DESCRIÇÃO')
pdf.drawString(390, 660, 'COD BARRA')
pdf.drawString(470, 660, 'QUANT')
pdf.drawString(520, 660, 'UNID')
pdf.line(30, 650, 555, 650)

def adicionarProdutos(produtos):
    x = [35, 100, 390, 510, 520]
    y = 640
    for produto in produtos:
        pdf.setFont('Helvetica', 10)
        pdf.drawString(x[0], y, produto.codigo_fabrica[5:])
        pdf.drawString(x[1], y, produto.descricao)
        pdf.setFont('Helvetica', 9)
        pdf.drawString(x[2], y, produto.codigo_barras)
        pdf.setFont('Helvetica', 10)
        pdf.drawRightString(x[3], y, f'{produto.quantidade}')
        pdf.drawString(x[4], y, produto.unidade)
        
        pdf.line(30, y-10, 555, y-10)

        y -= 20

    pdf.line(30, 650, 30, y+10)
    pdf.line(555, 650, 555, y+10)

def salvar():
    pdf.save()