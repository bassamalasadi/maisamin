from fpdf import FPDF
from datetime import date, datetime


class GenerateInvoice(FPDF):
    TEXT1= """
Saajan \n
tilinumero \n
Mottagrens \n
kontonummer \n
    """

    def __init__(self, *args, **kwargs):
        self.date = date.today()
        self.delivery_date = kwargs.get('delivery_date', 'Error')
        self.user_id = kwargs.get('user_id', 'Error')
        self.lasku_id = kwargs.get('lasku_id', 'Error')
        self.fname = kwargs.get('fname', 'Error')
        self.lname = kwargs.get('lname', 'Error')
        self.address = kwargs.get('address', 'Error')
        self.email = kwargs.get('email', 'Error')
        self.store = kwargs.get('store', 'Error')
        self.total = kwargs.get('total', 'Error')
        self.delivery_way = kwargs.get('delivery_way', 'Nouto')
        self.vat = kwargs.get('vat', 'Error')
        self.final = kwargs.get('final', 'Error')
        self.refrence = kwargs.get('refrence', 'Error')
        super().__init__()

    def header(self):
        self.image('static/img/logo2.jpg', 10, 8, 25)
        self.set_font('courier', 'B', 20)
        self.cell(0, 10, 'Maisamin Herkku', border=False, ln=1, align='C')
        self.image(f'{self.fname} {self.lname}.jpg', 150, 72, 45)
        self.ln(20)

    def footer(self):
        self.set_y(-65)
        self.set_margin(50)
        self.set_font('courier', '', 10)
        self.line(0, 232, 225, 232)
        self.set_x(10)
        self.set_font('courier', '', 6)
        # self.cell(20, 10, 'Saajan', border=1)
        # Save top coordinate
        top = self.y
        offset = self.x + 40
        self.multi_cell(30, 1, self.TEXT1, 'RB', 'R',)
                # Reset y coordinate
        self.y = top
        self.x = offset
        self.set_font('courier', '', 10)
        self.cell(155, 10, """  S-Pankki                         IBAN: FI32 3939 0054 3954 05""", 'B', ln=1)
        self.set_x(10)
        self.set_font('courier', '', 7)
        self.cell(20, 10, 'Saaja ', border=1)
        self.set_font('courier', 'B', 10)
        self.cell(65, 10, '  Maisamin Herkku', border=1, )
        self.set_x(95)
        self.set_font('courier', '', 10)
        self.cell(
            95, 10, 'MAKSETTAESSA ON KÄYTETTÄVÄ VIITENUMEROA', ln=1)
        self.set_x(95)
        self.set_font('courier', '', 7)
        self.cell(20, 10, ' Viitenumero ', border=1)
        self.set_font('courier', 'B', 11)
        self.cell(80, 10, f'{self.refrence}',
                  border=1, ln=1, align='R')
        self.set_x(10)
        self.set_font('courier', '', 7)
        self.cell(20, 10, 'Maksaja', border=1, align='C')
        self.set_font('courier', '', 9)
        self.cell(65, 10, f'{self.fname} {self.lname}', align='C')
        self.line(30, 272, 95, 272)
        self.set_font('courier', '', 7)
        self.cell(20, 10, """ Eräpäivä """, border=1)
        self.set_font('courier', 'B', 12)
        self.cell(40, 10, f'  {self.delivery_date}  ', border=1, align='R')
        self.cell(40, 10, f'   {self.total} ', border=1, align='R')
        self.set_font('courier', '', 7)
        self.cell(10, 10, 'EURO', ln=1)




def create_invoice(**kwargs):
    pdf = GenerateInvoice('P', 'mm', 'Letter', **kwargs)
    pdf.add_page()

    pdf.line(10, 30, 210, 30)
    pdf.set_font('courier', '', 8)
    pdf.cell(0, 3, 'Maisamin Herkku', ln=1)
    pdf.cell(0, 3, 'Asessorintie 2 11', ln=1)
    pdf.cell(0, 3, '32100 Jämsä', ln=1)
    pdf.cell(0, 3, 'maisaminherkku.fi', ln=1)
    pdf.cell(0, 3, 'info@maisamin.com', ln=1)
    pdf.cell(0, 3, '0405177444', ln=1)
    pdf.ln()

    pdf.set_font('courier', 'B', 11)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(0, 10, f'LASKU', ln=1, fill=1)
    pdf.set_font('courier', '', 10)
    pdf.cell(0,5, f'Asiakasnumero                    {pdf.user_id}', ln=1)
    pdf.cell(0,5, f'Laskunumero                      {pdf.lasku_id}', ln=1)
    pdf.cell(0, 5, f'laskunpäivämäärä                 {date.today()}', ln=1)
    pdf.cell(0, 5, f'Maksutapa                        Lasku', ln=1)
    pdf.cell(0, 5, f'Eräpäivä                         {pdf.delivery_date}', ln=1)
    pdf.ln()

    # payer

    pdf.set_fill_color(210, 210, 210)
    pdf.set_font('courier', 'B', 11)
    pdf.cell(0, 10, 'MAKSAJA', ln=1, fill=1)
    pdf.set_font('courier', '', 9)
    pdf.cell(0, 5, f'ATTN:{pdf.fname} {pdf.lname}', ln=1)
    pdf.cell(0, 5, f'{pdf.address}', ln=1)

    pdf.cell(0, 5, f'Verkkolaskutusosoite: {pdf.email}', ln=1)
    pdf.ln()
    pdf.ln()

    # products

    pdf.set_x(20)
    pdf.set_fill_color(250, 250, 250)
    pdf.set_font('courier', 'B', 10)
    pdf.cell(75, 7, 'TUOTE', border=1, fill=1)
    pdf.cell(50, 7 , 'G&L', border=1, fill=1)
    pdf.cell(15, 7, ' KPL', border=1, fill=1)
    pdf.cell(30, 7, ' Yhteensä', border=1, ln=1, align='C', fill=1)
    pdf.set_font('courier', '', 9)

    for value in pdf.store:
        pdf.set_x(20)
        pdf.cell(75, 6, f'  {value[0]}')
        pdf.cell(50, 6, f'  {value[1]}', align='C')
        pdf.cell(15, 6, f'  {value[3]}', align='C')
        pdf.cell(30, 6, f'EUR   {value[4]}', border=1, ln=1, align='C')

    pdf.set_x(20)
    pdf.set_font('courier', 'B', 10)
    pdf.cell(140, 5, 'Toimitus', border=1, fill=1)
    pdf.cell(30, 5, f'EUR   {pdf.delivery_way}', border=1, ln=1, align='C', fill=1)
    # pdf.set_x(20)
    # pdf.set_font('courier', 'B', 10)
    # pdf.cell(150, 5, 'Välisumma', border=1, fill=1)
    # pdf.cell(20, 5, f'{pdf.total}', border=1, ln=1, align='C', fill=1)
    # pdf.set_x(20)
    # pdf.set_font('courier', 'B', 10)
    # pdf.cell(150, 5, '24.00% alv', border=1, fill=1)
    # pdf.cell(20, 5, f'0.00', border=1, ln=1, align='C', fill=1)
    pdf.set_x(20)
    pdf.set_font('courier', 'B', 10)
    pdf.cell(140, 8, 'SUMMA', border=1, fill=1)
    pdf.cell(30, 8, f'EUR   {pdf.total}', border=1, ln=1, align='C', fill=1)
    pdf.ln()
    pdf.ln()

    pdf.output(f'{pdf.fname} {pdf.lname}.pdf')
