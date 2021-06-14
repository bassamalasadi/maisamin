from django import forms
import datetime
from django import forms
from allauth.account.forms import LoginForm, PasswordField , SignupForm

CITIES = (
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
    ('Cash', 'Käteinen'),
    ('Invoice', 'lasku  (Tilaus maksettava viimeistään 2 päivää ennen toimitusta)')
)

x = datetime.datetime.now() + datetime.timedelta(days=3)



class CheckoutForm(forms.Form):
    firstName = forms.CharField(required=True,
                                label='',
                                widget=forms.TextInput(attrs={'placeholder': 'Etunimi '}))
    lastName = forms.CharField(required=True,
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Sukunimi'}))
    city = forms.ChoiceField(choices=CITIES,
                             label='')
    street_address = forms.CharField(required=True,
                                     label='',
                                     widget=forms.TextInput(attrs={'placeholder': 'Osoite'}))
    apartment_address = forms.CharField(required=False,
                                        label='',
                                        widget=forms.TextInput(attrs={'placeholder': 'Huoneisto, Yksikkö jne. (valinnainen)'}))
    postal = forms.CharField(required=True,
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
                               widget=forms.TextInput(attrs={'placeholder': 'Valitse noutopäivä',
                                                             'start_date': x,
                                                             'readonly':'readonly'}))


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
        self.fields["password2"].label = ""
