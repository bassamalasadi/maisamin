from datetime import datetime, timedelta
from tabulate import tabulate
from django.core.mail import EmailMultiAlternatives

def geneartepdf(value):
    order = []
    count = 0
    for x in range(1, 5):
        if (value.POST.get(f"product_{x}")):
            order.append([(value.POST.get(f"product_{x}")), '', '', (value.POST.get(f"quantity_{x}")),(value.POST.get(f"price_{x}"))])
    return order

def send_email_if_reference_number_list_empty(value, sender, receiver ):
    if (len(value) <= 5):
         subject = f'Warning Maisamin Herkkuun'
         text_content = "Change refrence number"
         email_to_bassam = EmailMultiAlternatives(
             subject, text_content, sender, [receiver,],
         )
         email_to_bassam.send(fail_silently=False)

def is_valid_form(values):
    for field in values:
        if field == '' or len(str(field)) < 3:
            return False
    return True

def queryset_to_list(values):
    new_str = ""
    for value in values:
        value = str(value)
        new_str = new_str + value + ' - ' + '\n'
    return new_str

def order_list_for_email(order_item):
    order_email =[]
    for order in list(order_item):
        g = "Gluteeniton" if order.is_gluteen_free else ""
        l = "Laktoositon" if order.is_loctose_free else ""
        add_info = order.additional_info if order.additional_info else ""
        res = [str(order.product), g + " "+ l , add_info, order.quantity, "{:.2f}".format(order.get_total_product_price)]
        order_email.append(res)
    return order_email

def get_total_price(items):
    total = 0
    for order in items:
        total += float(order.get_final_price)
    total = "{:.2f}".format(total)
    return total

def modify_date(value):
    year = int(value[6:11])
    month = int(value[3:5])
    day = int(value[0:2])

    return (year, month, day)

def validating_date(date):
    year, month, day = modify_date(date)
    return datetime(year, month, day)

def modify_due_date(value):
    due_date = value.strftime('%Y-%m-%d')
    due_date = due_date.split('-')
    due_date = due_date[::-1]
    return '.'.join(due_date)

def get_picking_date_in_str(value):
    date = str(value)[0:10]
    date = date.split('-')
    date = date[::-1]
    return ".".join(date)

def get_invoice_option(**kwargs):
    refrence = kwargs['refrence']
    amount = kwargs['amount']
    due_date = kwargs['due_date']
    return f"""<br>
Saajan IBAN: <b> FI32 3939 0054 3954 05</b>  <br>
Viitenumero: <b>{refrence}</b> <br>
Yhteensä: <b>{amount} EUR </b><br>
Eräpäivä:<b> {due_date}</b> <br>
    """


# Tilaus:
# <hr>
# {tabulate(order_email,headers=["Kuvaus","Gluteeniton", "Lisää tiedot","Määrä","Yhteensä"], tablefmt='html')}
#
# <br>

def html_response_invoice(**kwargs):
    req_order = kwargs.get('req_order', '')
    date = kwargs.get('date', '')
    address = kwargs.get('address', '')
    email = kwargs.get('email', '')
    order_email = kwargs.get('order_email', '')
    deliv = kwargs.get('deliv', '')
    amount = kwargs.get('amount', '')
    pay = kwargs.get('pay', '')
    return f""" <h4>Kiitos, että valitsit Maisamin Herkun.</h4> <br>
Tilauksesi numero : <b>{req_order}</b><br>
Toimitetaan : <b>{date}</b> <br>
Osoitteeseen : <b>{address}</b> <br>
Verkkolaskutusosoite : <b>{email}</b> <br>

<br>

{deliv}
<br>
<b>Yhteensä: {amount} EURO</b>
<hr>
{pay}
<br>
<hr>
<h4>HUOM!</h4> Peruutus on suoritettava vähintään kaksi vuorokautta ennen tilauksen toimituspäivää.
Jos haluat peruuttaa tilauksesi, Lähetä viesti "Peruuta ja tilauksen numero "<b>{req_order}</b> "numeroon 0405177444 tai sähköpostia osoitteeseen <b>Info@maisaminherkku.fi</b>  <br>
Kiitos
    """

def confirmation_email_to_user():
    return f"""
<h4>Kiitos, että valitsit Maisamin Herkun.</h4> <br>
<h4>Tilauksesi käsitellään pian. Saat vahvistussähköpostin mahdollisimman pian.</h4><br>
<img src="https://www.maisaminherkku.fi/static/img/brand_logo_1.svg" alt="M">
    """
