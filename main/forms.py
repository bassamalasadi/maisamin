from django import forms
import datetime
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
    ('Cash', 'Käteinen raha'),
    ('Invoice', 'lasku')
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
                                     widget=forms.TextInput(attrs={'placeholder': 'Kadunnimi ja Talon numero'}))
    apartment_address = forms.CharField(required=False,
                                        label='',
                                        widget=forms.TextInput(attrs={'placeholder': 'Huoneisto, Yksikkö jne. (valinnainen)'}))
    postal = forms.CharField(required=True,
                             label='',
                             widget=forms.TextInput(attrs={'placeholder': 'Postinumer'}))
    email = forms.EmailField(required=True,
                             label='',
                             widget=forms.TextInput(attrs={'placeholder': 'Sähköpostiosoite'}))
    phone = forms.CharField(required=True,
                            label='',
                            widget=forms.TextInput(attrs={'placeholder': 'Puhelin'}))
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Valitse noutopäivä',
                                                             'start_date': x}))

    payment_option = forms.ChoiceField(required=True,
                                       label='',
                                       widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)
