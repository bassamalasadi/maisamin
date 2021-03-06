import datetime
from django import forms
from allauth.account.forms import LoginForm, PasswordField , SignupForm
from django.contrib.auth.models import User
from django.core import validators

CITIES = (
    ('Kaupunki', 'Kaupunki'),
    ('Jämsä', 'Jämsä'),
    ('Jämsänkoski', 'Jämsänkoski'),
    ('Kaipola', 'Kaipola'),
    ('Halli', 'Halli'),
    ('Koskenpää', 'Koskenpää'),
    ('Länkipohja', 'Länkipohja'),
    ('Himos', 'Himos'),
    ('Korpilahti', 'Korpilahti'),
    ('Muurame', 'Muurame'),
    ('Jyväskylä', 'Jyväskylä')
)

PAYMENT_CHOICES = (
    ('Cash', 'Käteinen / MobilePay'),
    ('Invoice', 'Lasku  (Tilaus maksettava viimeistään 2 päivää ennen toimitusta)'),
)

x = datetime.datetime.now() + datetime.timedelta(days=3)


class GenerateInvoiceForm(forms.Form):
    firstName = forms.CharField(required=True,
                                label='',
                                widget=forms.TextInput(attrs={'placeholder': 'FirstName'}))
    lastName = forms.CharField(required=True,
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': 'LastName'}))

    user_id  = forms.CharField(required=False,
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': 'User ID'}))
    invoice_id  = forms.CharField(required=False,
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Invoice ID'}))
    date = forms.DateTimeField(required=True,
                               input_formats=['%d/%m/%Y %H:%M'],
                               label='',
                               widget=forms.TextInput(attrs={
                                                             'placeholder': 'Date',
                                                             'start_date': x,
                                                             'pattern':'^(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/](19|20)\d\d$'
                                                             }),
                                                      )
    address = forms.CharField(required=False,
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    postal = forms.CharField(required=False,
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Postal'}))
    email = forms.EmailField(required=False,
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': 'email'}))
    product_1  = forms.CharField(required=True,
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Product'}))
    product_2  = forms.CharField(required=False,
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Product'}))
    product_3  = forms.CharField(required=False,
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Product'}))
    product_4  = forms.CharField(required=False,
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Product'}))


class CheckoutForm(forms.Form):
    firstName = forms.CharField(required=True,
                                label='',
                                widget=forms.TextInput(attrs={'placeholder': 'Etunimi '}))
    lastName = forms.CharField(required=True,
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Sukunimi'}))
    city = forms.ChoiceField(choices=CITIES,
                             label='')
    street_address = forms.CharField(required=False,
                                     label='',
                                     widget=forms.TextInput(attrs={'placeholder': 'Osoite'}))
    apartment_address = forms.CharField(required=False,
                                        label='',
                                        widget=forms.TextInput(attrs={'placeholder': 'Huoneisto, Yksikkö jne. (valinnainen)'}))
    postal = forms.CharField(required=False,
                             label='',
                             widget=forms.TextInput(attrs={'placeholder': 'Postinumero'}))
    email = forms.EmailField(required=True,
                             label='',
                             widget=forms.TextInput(attrs={'placeholder': 'Sähköpostiosoite'}))
    phone = forms.CharField(required=True,
                            label='',
                            widget=forms.TextInput(attrs={'placeholder': 'Puhelin'}))
    date = forms.DateTimeField(required=True,
                               input_formats=['%d/%m/%Y %H:%M'],
                               label='',
                               widget=forms.TextInput(attrs={
                                                             'placeholder': 'Valitse noutopäivä',
                                                             'start_date': x,
                                                             'pattern':'^(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/](19|20)\d\d$'
                                                             }),
                                                      )
    payment_option = forms.ChoiceField(required=True,
                                       label='',
                                       widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)


class SelfLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["login"].label = ""
        self.fields["password"].label = ""

class SelfSignUpForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].label = ""
        self.fields["username"].label = ""
        self.fields["password1"].label = ""
