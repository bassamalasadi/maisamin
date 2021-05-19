from fpdf import FPDF
from datetime import date, datetime


class GenerateInvoice(FPDF):

    def __init__(self, *args, **kwargs):
        self.date = date.today()
        self.delivery_date = kwargs.get('delivery_date', 'Error')
        self.fname = kwargs.get('fname', 'Error')
        self.lname = kwargs.get('lname', 'Error')
        self.address = kwargs.get('address', 'Error')
        self.email = kwargs.get('email', 'Error')
        self.store = kwargs.get('store', 'Error')
        self.totel = kwargs.get('totel', 'Error')
        self.delivery_way = kwargs.get('delivery_way', 'Nouto')
        self.vat = kwargs.get('vat', 'Error')
        self.final = kwargs.get('final', 'Error')
        super().__init__()

    def header(self):
        self.image('static_style/img/logo2.png', 10, 8, 25)
        self.set_font('courier', '', 16)
        self.cell(0, 10, 'Lasku', border=False, ln=1, align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-65)
        self.set_margin(50)
        self.set_font('courier', '', 10)
        self.line(0, 232, 225, 232)
        self.set_x(10)
        self.set_font('courier', '', 7)
        self.cell(20, 10, '    Saajan ', border=1)
        self.set_font('courier', '', 10)
        self.cell(
            165, 10, """  Osuuspankki                         FI03 1025 3000 2593 51""", border=1, ln=1)
        self.set_x(10)
        self.set_font('courier', '', 7)
        self.cell(20, 10, '     Saaja  ', border=1)
        self.set_font('courier', 'B', 10)
        self.cell(65, 10, '  MAISAMIN HERKKU Oy', border=1, )
        self.set_x(95)
        self.set_font('courier', '', 10)
        self.cell(
            95, 10, 'MAKSETTAESSA ON KÄYTETTÄVÄ VIITENUMEROA', ln=1)
        self.set_x(95)
        self.set_font('courier', '', 7)
        self.cell(20, 10, ' Viitenumero ', border=1)
        self.set_font('courier', 'B', 11)
        self.cell(80, 10, f'{str(datetime.timestamp(datetime.now())).replace(".", "")}',
                  border=1, ln=1, align='R')
        self.set_x(10)
        self.set_font('courier', '', 7)
        self.cell(20, 10, 'Maksaja', border=1, align='C')
        self.set_font('courier', '', 9)
        self.cell(65, 10, f'{self.fname} {self.lname}', align='C')
        self.line(30, 272, 95, 272)
        self.set_font('courier', '', 7)
        self.cell(20, 10, ' Eräpäivä ', border=1)
        self.set_font('courier', 'B', 12)
        self.cell(40, 10, f'  {self.delivery_date}  ', border=1, align='R')
        self.cell(40, 10, f'   {self.final} ', border=1, align='R')
        self.set_font('courier', '', 7)
        self.cell(10, 10, 'EURO')


def create_invoice(**kwargs):
    pdf = GenerateInvoice('P', 'mm', 'Letter', **kwargs)
    pdf.add_page()

    pdf.line(10, 30, 210, 30)
    pdf.set_font('courier', '', 8)
    pdf.cell(0, 3, 'Asessorintie 2 11', ln=1)
    pdf.cell(0, 3, '32100 Jämsä', ln=1)
    pdf.cell(0, 3, 'maisaminherkku.fi', ln=1)
    pdf.cell(0, 3, 'info@maisamin.com', ln=1)
    pdf.cell(0, 3, '0405177444', ln=1)
    pdf.ln()

    pdf.set_font('courier', 'B', 11)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(0, 10, f'Lasku:', ln=1, fill=1)
    pdf.set_font('courier', '', 10)
    pdf.cell(0, 5, f'Laskun päivöys: {date.today()}', ln=1)
    pdf.cell(0, 5, f'Eräpäivä: {pdf.delivery_date}', ln=1)
    pdf.ln()

    # payer

    pdf.set_fill_color(210, 210, 210)
    pdf.set_font('courier', 'B', 11)
    pdf.cell(0, 10, 'Maksaja', ln=1, fill=1)
    pdf.set_font('courier', '', 9)
    pdf.cell(0, 5, f'ATTN:{pdf.fname} {pdf.lname}', ln=1)
    pdf.cell(0, 5, f'{pdf.address}', ln=1)

    pdf.cell(0, 5, f'Verkkolaskutusosoite: {pdf.email}', ln=1)
    pdf.ln()
    pdf.ln()

    # products

    pdf.set_x(20)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('courier', 'B', 10)
    pdf.cell(130, 7, 'Kuvaus', border=1, fill=1)
    pdf.cell(20, 7, 'Määrä', border=1, fill=1)
    pdf.cell(20, 7, 'Yhteensä', border=1, ln=1, align='C', fill=1)
    pdf.set_font('courier', '', 9)

    for value in pdf.store:
        pdf.set_x(20)
        pdf.cell(130, 6, f'{value[0]}')
        pdf.cell(20, 6, f'{value[1]}', align='C')
        pdf.cell(20, 6, f'{value[2]}0', border=1, ln=1, align='C')
    pdf.set_x(20)
    pdf.set_font('courier', 'B', 10)
    pdf.cell(150, 5, 'Toimitus', border=1, fill=1)
    pdf.cell(20, 5, f'{pdf.delivery_way}', border=1, ln=1, align='C', fill=1)
    pdf.set_x(20)
    pdf.set_font('courier', 'B', 10)
    pdf.cell(150, 5, 'Välisumma', border=1, fill=1)
    pdf.cell(20, 5, f'{pdf.totel}', border=1, ln=1, align='C', fill=1)
    pdf.set_x(20)
    pdf.set_font('courier', 'B', 10)
    pdf.cell(150, 5, '24.00% alv', border=1, fill=1)
    pdf.cell(20, 5, f'{pdf.vat}', border=1, ln=1, align='C', fill=1)
    pdf.set_x(20)
    pdf.set_font('courier', 'B', 10)
    pdf.cell(150, 8, 'Yhteensä', border=1, fill=1)
    pdf.cell(20, 8, f'{pdf.final}', border=1, ln=1, align='C', fill=1)
    pdf.ln()
    pdf.ln()

    pdf.output(f'{pdf.fname} {pdf.lname}.pdf')
