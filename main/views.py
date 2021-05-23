import os

from datetime import datetime, timedelta

from django.core.mail import send_mail, EmailMessage
from django.conf import settings

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponseBadRequest

from django.utils.translation import ugettext as _

from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView, View
from rest_framework import viewsets
from .serializers import ItemSerializer

from .forms import CheckoutForm
from django.utils.formats import sanitize_separators
from django.contrib.auth.models import User
from .models import Product, OrderItem, Order, Request, UserProfile
from .lasku import create_invoice

from tabulate import tabulate


class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser


class ItemView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Product.objects.all()


def modify_date(value):
    year = int(value[6:11])
    month = int(value[3:5])
    day = int(value[0:2])

    return (year, month, day)


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


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order
            }
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, _("Sinulla ei ole aktiivista tilausta"))
            return redirect("main:home")

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        pay = 'Maksat, kun tilaus toimitetaan tai noudetaan '
        try:
            order_item = Order.objects.get(
                user=self.request.user, ordered=False)
            amount = order_item.get_total()
            product_order = order_item.get_items_detail
            if amount <= 0:
                messages.warning(self.request, "Empty cart")
                return redirect("main:checkout")
            if request.method == 'POST':
                req = request.POST
                year, month, day = modify_date(req.get('date'))
                firstName = req.get('firstName')
                lastName = req.get('lastName')
                city = req.get('city')
                street_address = req.get('street_address')
                apartment_address = req.get('apartment_address')
                postal = req.get('postal')
                phone = req.get('phone')
                email = req.get('email')
                address = str(city) + ' - ' + str(street_address) + \
                    ' - ' + str(apartment_address)
                date = datetime(year, month, day)
                delivery_date = date - timedelta(days=2)
                due_date = delivery_date.strftime('%Y-%m-%d')
                delivery = req.get('delivery')
                refrence = str(datetime.timestamp(
                    datetime.now())).replace(".", "")

                if req.get('deliver') != 0 or req.get('delivery') != 1:
                    amount = float(order_item.get_total()) + \
                        float(req.get('delivery'))
                vat = float(amount) * 0.24
                final = amount + vat
                final = "{:.2f}".format(final)
                vat = "{:.2f}".format(vat)
                amount = "{:.2f}".format(amount)
                if req.get('payment_option') == 'Invoice':
                    pay = f"""
                        Saajan IBAN: FI19 5091 0320 1303 46  \n
                        Viitenumero: {refrence} \n
                        Yhteensä: {final}0 EURO \n
                        Eräpäivä: {due_date} \n
                    """
                if is_valid_form([firstName, lastName, city, street_address,
                                  postal, phone, email,
                                  date, pay]):
                    order_list = queryset_to_list(
                        list(order_item.products.all()))
                    req = Request.objects.create(
                        name=firstName,
                        address=address,
                        phone=phone,
                        email=email,
                        order=order_list,
                        create=datetime.now(),
                        delivery=date,
                        delivery_price=delivery,
                    )

                    create_invoice(
                        delivery_date=due_date,
                        fname=firstName,
                        lname= lastName,
                        address=address,
                        email=email,
                        store=product_order,
                        totel=amount,
                        refrence=refrence,
                        delivery_way=delivery,
                        vat=vat,
                        final=final
                    )
                    subject = f'Tervetuloa {firstName} {lastName} Maisamin Herkkuun'
                    message = f""" Moi, {lastName}  \n
Kiitos, että valitsit Maisamin Herkun. \n
Tilauksesi numero : {req.id} \n
Toimitetaan : {str(date)[0:10]} \n
Osoitteeseen : {address} \n
____________________________________________________________________________________________________ \n
Tilaus: \n

{tabulate(product_order,headers=["Kuvaus","Määrä","Yhteensä"], tablefmt='rst', colalign=("right",))}

____________________________________________________________________________________________________ \n
Huom! Jos haluat peruuttaa tilauksesi, lähetä: (tilausnumero: {order_item.id}, Viitenumero: {refrence}, ja "Peruuttaa") tähän puhelinnumeroon: 0405177444
tai sähköpostiosoitteeseen:  Info@maisaminherkku.fi  \n
____________________________________________________________________________________________________ \n
{pay}
Kiitos
                    """

                    recepient = email
                    email = EmailMessage(
                        subject, message, settings.EMAIL_HOST_USER, [
                            recepient, settings.EMAIL_HOST_USER],
                    )
                    email.attach_file(f'{firstName} {lastName}.pdf')
                    email.send(fail_silently=False)

                    try:
                        os.remove(f'{firstName} {lastName}.pdf')
                        OrderItem.objects.filter(user=self.request.user).delete()
                    except:
                        pass
                else:
                    messages.warning(self.request, "Virheellinen muoto, kentän tulee sisältää enemmän kuin kaksi merkkiä eikä olla tyhjä")
                    return redirect("main:checkout")
            else:
                messages.warning(self.request, "Virheellinen lomake")
                return redirect("main:checkout")
            context = {
                'form': form
            }
            return render(self.request, "message.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Sinulla ei ole tilausta")
            return redirect("main:order-summary")


class HomeView(ListView):
    model = Product
    paginate_by = 10
    template_name = "home.html"


class CakeView(ListView):
    model = Product
    paginate_by = 10
    template_name = "cake.html"


class CheeseCakeView(ListView):
    model = Product
    paginate_by = 10
    template_name = "cheesecake.html"


class FatayerView(ListView):
    model = Product
    paginate_by = 10
    template_name = "fatayer.html"


class ManakishView(ListView):
    model = Product
    paginate_by = 10
    template_name = "manakish.html"


class MezeView(ListView):
    model = Product
    paginate_by = 10
    template_name = "meze.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)
            order_item = OrderItem.objects.filter(user=self.request.user)
            context = {
                'object': order,
                'product': order_item,
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(
                self.request, "Sinulla ei ole aktiivista tilausta")
            return redirect("/")


class Profile(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            user = User.objects.get(username=self.request.user)

            context = {
                'user': user,
            }
            return render(self.request, 'profile.html', context)
        except ObjectDoesNotExist:
            messages.warning(
                self.request, "käyttäjää ei löydy")
            return redirect("/")

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if 'edit' in request.POST:
                username = request.POST.get('username')
                email  = request.POST.get('email')
                user = User.objects.get(username=self.request.user)
                if user.username != username or user.email != email:
                    try:
                        user.username = username
                        user.email = email
                        user.save()
                        messages.success(
                            self.request, "Käyttäjätunnuksen tai sähköpostiosoitteen muuttaminen onnistui")
                        return redirect("main:profile")
                    except:
                        messages.success(
                            self.request, "käyttäjänimi tai sähköpostiosoite on jo olemassa")
                        return redirect("main:profile")
                else:
                    messages.warning(
                        self.request, "käyttäjänimi ja sähköpostiosoite eivät muutu")
                return redirect("main:profile")
            if 'delete' in request.POST:
                try:
                    user = User.objects.get(username=self.request.user)
                    user.delete()
                    messages.success(self.request, "Käyttäjä on poistettu")
                    return redirect("/")
                except User.DoesNotExist:
                    messages.warning(
                        self.request, "Virhe. Anteeksi, yritä lähettää sähköpostia osoitteeseen info@maisaminherkku.com"
                    )
                    return redirect("main:profile")

                return render(self.request, '/')

class ClientOrder(LoginRequiredMixin,
                  SuperUserCheck,
                  ListView):
    paginate_by = 10
    template_name = "clientorder.html"

    def get_queryset(self):
        return Request.objects.filter(delivery__gt=datetime.now())


class OrderDetail(LoginRequiredMixin,
                  SuperUserCheck,
                  DetailView):
    model = Request
    paginate_by = 10
    template_name = "order_detail.html"


class ItemDetailView(View):

    def get(self, *args, **kwargs):
        try:
            product = get_object_or_404(Product, slug=kwargs['slug'])
            context = {
                'product': product
            }
            return render(self.request, "product.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "not working")
            return redirect("main:home")

    def post(self, request, slug):
        price = sanitize_separators(request.POST.get('price'))
        amount = sanitize_separators(request.POST.get('amount'))
        gluteen = sanitize_separators(request.POST.get('gluteen'))
        laktoos = sanitize_separators(request.POST.get('laktoos'))
        product = get_object_or_404(Product, slug=slug)
        if request.user.is_anonymous:
            return redirect('account_login')
        else:
            try:
                order_product, created = OrderItem.objects.get_or_create(
                    product=product,
                    user=request.user,
                    ordered=False,
                    price=price,
                    is_gluteen_free=isinstance(gluteen ,str),
                    is_loctose_free=isinstance(laktoos ,str),
                )

                order_qs = Order.objects.filter(
                    user=self.request.user, ordered=False)

                if order_qs.exists():
                    order = order_qs[0]
                    # check if the order item is in the order
                    if order.products.filter(product__slug=product.slug, price=price).exists():
                        order_product.quantity += int(amount) - 1
                        if gluteen:
                            order_product.is_gluteen_free = True
                        if laktoos:
                            order_product.is_loctose_free = True
                        order_product.save()
                        messages.info(
                            self.request, "Tämä tuote lisättiin ostoskoriin")
                        return redirect("main:product", slug=slug)
                    else:
                        if int(amount) > 1:
                            order_product.quantity += int(amount) - 1
                            if gluteen:
                                order_product.is_gluteen_free = True
                            if laktoos:
                                order_product.is_loctose_free = True
                            order_product.save()
                        order.products.add(order_product)
                        messages.info(
                            self.request, "Tämä tuote lisättiin ostoskoriin")
                        return redirect("main:product", slug=slug)
                else:
                    order = Order.objects.create(
                        user=self.request.user)
                    order.products.add(order_product)
                    messages.info(
                        self.request, "Tämä tuote lisättiin ostoskoriin")
                    return redirect("main:product", slug=slug)
            except:
                HttpResponseBadRequest()


@ login_required
def add_to_cart(request, slug, **kwargs):
    print("#############", kwargs)
    product = get_object_or_404(Product, slug=slug)
    if kwargs:
        price = request.POST.get('price') or kwargs['price']
    else:
        price = product.price

    order_product, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
        price=price
    )
    order_qs = Order.objects.filter(
        user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug, price=price).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "Tämä tuote lisättiin ostoskoriin")
            return redirect("main:order-summary")

        else:
            order.products.add(order_product)
            messages.info(request, "Tämä tuote lisättiin ostoskoriin")
            return redirect("main:order-summary")
    else:
        order = Order.objects.create(
            user=request.user)
        order.products.add(order_product)
        messages.info(request, "Tämä tuote lisättiin ostoskoriin")
        return redirect("main:order-summary")


@ login_required
def remove_single_item_from_cart(request, slug, **kwargs):
    product = get_object_or_404(Product, slug=slug)
    if kwargs['price']:
        price = kwargs['price']
    else:
        price = product.price

    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(product__slug=product.slug, price=price).exists():
            order_product = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False,
                price=price
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
            return redirect("main:order-summary")
        else:
            messages.info(request, "Tätä tuotetta ei ollut ostoskorissa")
            return redirect("main:order-summary")
    else:
        messages.info(request, "Sinulla ei ole tilausta")
        return redirect("main:home")


@ login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_product)
            order_product.delete()
            messages.info(request, "Tämä tuote poistettiin ostoskorista")
            return redirect("main:order-summary")
        else:
            messages.info(request, "Tätä tuotetta ei ollut ostoskorissa")
            return redirect("main:product", slug=slug)
    else:
        messages.info(request, "Sinulla ei ole tilausta")
        return redirect("main:product", slug=slug)


@ user_passes_test(lambda u: u.is_superuser)
def remove_from_order_page(request, pk):
    order = get_object_or_404(Request, pk=pk)
    if order:
        order.delete()
        messages.info(request, 'Tämä tuote on poistettu')
        return redirect("main:client-order")
    else:
        messages.info(request, 'Sinulla ei ole poistettavaa tuotetta ')
        return redirect("main:client-order")


class Privacy(View):
    def get(self, *args, **kwargs):
        return render(self.request, "privacy-policy.html")
