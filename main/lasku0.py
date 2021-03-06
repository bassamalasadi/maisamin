from fpdf import FPDF
from datetime import date, datetime


class GenerateInvoice(FPDF):
    TEXT1 = """
Saajan \n
tilinumero \n
Mottagrens \n
kontonummer \n
    """

    TEXT2 = """
IBAN \n
\n
FI32 3939 0054 3954 05 \n
\n
    """

    TEXT3 = """
BIC \n
\n
SBANFIHH \n
\n
    """

    TEXT4 = """
Saaja \n
Mottagren \n
\n
\n
\n
\n
\n
    """

    TEXT5 = """
    \n
Maisamin Herkku \n
\n
Koskentie 42 \n
\n
42100 Jämsä\n
\n
    """
    TEXT5_5 = """
\n
Maksu käteisellä tai Mobile Paylla  \n
\n
(040 5177444) tilauksen toimituksen/noudon\n
\n
yhteydessä.
    """
    TEXT6 = """
\n
\n
\n
\n
    """
    TEXT7 = """
Maksajan \n
nimi ja osoite \n
Betalarens \n
namn och \n
address \n

    """
    TEXT9 = """
    \n
    \n
Allekirjoitus \n
Underskrift \n
\n
    """
    TEXT10 = """
\n
\n
\n
_______________________________________________________
    """
    TEXT11 = """
    \n
Viitenumero \n
Ref. nr \n
\n
    """
    TEXT12 = """
    \n
Tililtä nro \n
Från konto nr \n
\n
    """
    TEXT13 = """
    \n
Eräpäivä \n
FÖrfallodag \n
\n
    """

    def __init__(self, *args, **kwargs):
        self.date = date.today()
        self.pay_date = kwargs.get('pay_date', '')
        self.user_id = kwargs.get('user_id', '')
        self.lasku_id = kwargs.get('lasku_id', '')
        self.fname = kwargs.get('fname', '')
        self.lname = kwargs.get('lname', '')
        self.address = kwargs.get('address', '')
        self.postal = kwargs.get('postal', '')
        self.email = kwargs.get('email', '')
        self.store = kwargs.get('store', '')
        self.total = kwargs.get('total', '')
        self.delivery_way = kwargs.get('delivery_way', 'Nouto')
        self.vat = kwargs.get('vat', '')
        self.final = kwargs.get('final', '')
        self.refrence = kwargs.get('refrence', '')
        self.pay = kwargs.get('pay', '')
        self.pay_method = kwargs.get('pay_method', '')
        if self.pay_method == 'Lasku':
            TEXT5_5 = ''
        super().__init__()


    def header(self):
        self.image('static/img/brand_logo.JPG', 10, 8, 25)
        self.set_font('courier', 'B', 20)
        self.cell(0, 10, 'Maisamin Herkku', border=False, ln=1, align='C')
        self.image(f'{self.fname} {self.lname}.svg', 150, 72, 45)
        self.ln(20)

    def footer(self):
        name = f"""
\n
{self.fname} {self.lname} \n
{self.address} \n
{self.postal} \n
\n
        """
        refrence = f"""
\n
\n
{self.refrence} \n
\n
        """
        date = f"""
\n
\n
{self.pay_date} \n
\n
        """
        price = f"""
EUR\n
            \n
            {self.total} \n
            \n
        """
        self.set_y(-65)
        self.set_margin(50)
        self.set_x(40)
        self.line(0, 230, 225, 230)
        #
        self.set_font('courier', '', 6)
        self.set_x(10)
        top = self.y
        offset = self.x + 40
        self.multi_cell(30, 1, self.TEXT1, 'RB', 'R',)
        self.y = top
        self.x = offset
        #
        self.set_font('courier', '', 8)
        self.set_x(40)
        top = self.y
        offset = self.x + 40
        self.multi_cell(70, 1, self.TEXT2, 'RB', 'l',)
        self.y = top
        self.x = offset
        #
        self.set_font('courier', '', 8)
        self.set_x(110)
        top = self.y
        offset = self.x + 40
        self.multi_cell(90, 1, self.TEXT3, 'B', 'l', ln=1)
        self.y = top
        self.x = offset
        # #############
        self.set_y(-55)
        #
        self.set_font('courier', '', 6)
        self.set_x(10)
        top = self.y
        offset = self.x + 40
        self.multi_cell(30, 1, self.TEXT4, 'RB', 'R',)
        self.y = top
        self.x = offset
        #
        self.set_font('courier', '', 8)
        self.set_x(40)
        top = self.y
        offset = self.x + 40
        self.multi_cell(70, 1, self.TEXT5, 'RB', 'l',)
        self.y = top
        self.x = offset
        #
        self.set_font('courier', '', 8)
        self.set_x(110)
        top = self.y
        offset = self.x + 40
        self.multi_cell(95, 1, self.TEXT5_5, '', 'l', ln=1)
        self.y = top
        self.x = offset
        # #############
        self.set_y(-39)
        #
        self.set_font('courier', '', 6)
        self.set_x(10)
        top = self.y
        offset = self.x + 40
        self.multi_cell(30, 1, self.TEXT7, '', 'R',)
        self.y = top
        self.x = offset
        #
        self.set_font('courier', '', 7)
        self.set_x(40)
        top = self.y
        offset = self.x + 40
        self.multi_cell(70, 1, name, 'R', 'l',)
        self.y = top
        self.x = offset
        #
        self.set_font('courier', '', 8)
        self.set_x(110)
        top = self.y
        offset = self.x + 40
        self.multi_cell(95, 1, self.TEXT6, '', 'l', ln=1)
        self.y = top
        self.x = offset
        # #############
        self.set_y(-29)
        #
        self.set_font('courier', '', 6)
        self.set_x(10)
        top = self.y
        offset = self.x + 40
        self.multi_cell(30, 1, self.TEXT9, '', 'R',)
        self.y = top
        self.x = offset
        #
        self.set_font('courier', '', 5)
        self.set_x(40)
        top = self.y
        offset = self.x + 40
        self.multi_cell(70, 1, self.TEXT10, 'R', 'l',)
        self.y = top
        self.x = offset
        #
        self.set_font('courier', '', 6)
        self.set_x(110)
        top = self.y
        offset = self.x + 40
        self.multi_cell(20, 1, self.TEXT11, 'TBRL', 'l')
        self.y = top
        self.x = offset
        #
        self.set_font('courier', '', 8)
        self.set_x(130)
        top = self.y
        offset = self.x + 40
        self.multi_cell(70, 1, refrence, 'TB', 'l', ln=1)
        self.y = top
        self.x = offset
        # #############
        self.set_y(-19)
        #
        self.set_font('courier', '', 6)
        self.set_x(10)
        top = self.y
        offset = self.x + 40
        self.multi_cell(30, 1, self.TEXT12, 'TRB', 'R',)
        self.y = top
        self.x = offset
        #
        self.set_font('courier', '', 6)
        self.set_x(40)
        top = self.y
        offset = self.x + 40
        self.multi_cell(70, 1, self.TEXT6, 'TB', 'l',)
        self.y = top
        self.x = offset
        #
        self.set_font('courier', '', 6)
        self.set_x(110)
        top = self.y
        offset = self.x + 40
        self.multi_cell(20, 1, self.TEXT13, 'TBRL', 'l')
        self.y = top
        self.x = offset
        #
        self.set_font('courier', 'B', 7)
        self.set_x(130)
        top = self.y
        offset = self.x + 40
        self.multi_cell(30, 1, date, 'BR', 'l')
        self.y = top
        self.x = offset
        #
        self.set_font('courier', 'B', 7)
        self.set_x(160)
        top = self.y
        offset = self.x + 40
        self.multi_cell(40, 1, price, 'B', 'l', ln=1)
        self.y = top
        self.x = offset


def create_invoice(**kwargs):

    date_of_invoic = date.today()
    date_of_invoic = str(date_of_invoic).split('-')
    date_of_invoic = date_of_invoic[::-1]
    date_of_invoic = '.'.join(date_of_invoic)

    pdf = GenerateInvoice('P', 'mm', 'Letter', **kwargs)
    pdf.add_page()

    pdf.line(10, 30, 210, 30)
    pdf.set_font('courier', '', 8)
    pdf.cell(0, 3, 'Maisamin Herkku', ln=1)
    pdf.cell(0, 3, 'Koskentie 42', ln=1)
    pdf.cell(0, 3, '42100 Jämsä', ln=1)
    pdf.cell(0, 3, 'maisaminherkku.fi', ln=1)
    pdf.cell(0, 3, 'info@maisamin.fi', ln=1)
    pdf.cell(0, 3, '0405177444', ln=1)
    pdf.ln()

    pdf.set_font('courier', 'B', 11)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(0, 10, f'LASKU', ln=1, fill=1)
    pdf.set_font('courier', '', 10)
    pdf.cell(0,5, f'Asiakasnumero                    {pdf.user_id}', ln=1)
    pdf.cell(0,5, f'Laskunumero                      {pdf.lasku_id}', ln=1)
    pdf.cell(0, 5, f'Laskunpäivämäärä                 {date_of_invoic}', ln=1)
    pdf.cell(0, 5, f'Maksutapa                        {pdf.pay_method}', ln=1)
    pdf.cell(0, 5, f'Eräpäivä                         {pdf.pay_date}', ln=1)
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
    pdf.cell(50, 7 , 'Gluteeniton', border=1, fill=1)
    pdf.cell(15, 7, ' KPL', border=1, fill=1)
    pdf.cell(30, 7, ' Yhteensä', border=1, ln=1, align='C', fill=1)
    pdf.set_font('courier', '', 9)

    for value in pdf.store:
        pdf.set_x(20)
        pdf.cell(75, 6, f'  {value[0]}')
        pdf.cell(50, 6, f'  {value[1]}', align='L')
        pdf.cell(15, 6, f'  {value[3]}', align='L')
        pdf.cell(30, 6, f'EUR   {value[4]}', border=1, ln=1, align='C')

    pdf.set_x(20)
    pdf.set_font('courier', 'B', 10)
    pdf.cell(140, 5, 'Toimitus', border=1, fill=1)
    pdf.cell(30, 5, f' {pdf.delivery_way}', border=1, ln=1, align='C', fill=1)

    pdf.set_x(20)
    pdf.set_font('courier', 'B', 10)
    pdf.cell(140, 8, 'SUMMA', border=1, fill=1)
    pdf.cell(30, 8, f'EUR   {pdf.total}', border=1, ln=1, align='C', fill=1)
    pdf.ln()
    pdf.ln()

    pdf.output(f'{pdf.fname} {pdf.lname}.pdf')
