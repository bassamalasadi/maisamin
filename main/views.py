import os
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
from . import helper
from django.utils.formats import sanitize_separators
from django.contrib.auth.models import User
from .models import Product, OrderItem, Order, Request
from .lasku0 import create_invoice

from barcode import EAN13, Code39
from barcode.writer import ImageWriter

from django.http import HttpResponseRedirect, JsonResponse
from allauth.account.adapter import DefaultAccountAdapter

from django.core.mail import EmailMultiAlternatives

from .choices import REFRENCE_LIST


class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser


class ItemView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Product.objects.all()


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order_item = OrderItem.objects.filter(user=self.request.user, ordered=False)

            total = 0
            for order in order_item:
                total += float(order.get_final_price)
            total = "{:.2f}".format(total)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order_item,
                'object': total,
                'user': self.request.user,
            }
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, _("Sinulla ei ole aktiivista tilausta"))
            return redirect("main:home")

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        pay = 'Maksat, kun tilaus toimitetaan tai noudetaan '
        try:
            order_item = OrderItem.objects.filter(user=self.request.user, ordered=False)
            user = User.objects.get(username=self.request.user)
            amount = helper.get_total_price(order_item)
            if float(amount) <= 0:
                messages.warning(self.request, "Tyhjä ostoskori")
                return redirect("main:home")

            if request.method == 'POST' and form.is_valid:
                req = request.POST
                firstName = req.get('firstName')
                lastName = req.get('lastName')
                city = req.get('city', '')
                city = 'Osoite ei ole käytettävissä' if city == 'Kaupunki' else city
                street_address = req.get('street_address', '')
                apartment_address = req.get('apartment_address', '')
                postal = req.get('postal', '')
                phone = req.get('phone')
                email = req.get('email')
                address = str(city) + ' - ' + str(street_address) + '   ' + str(apartment_address)
                payment_option = req.get('payment_option')
                date = req.get('date')
                if date:
                    picking_date = helper.validating_date(date)
                    validate_date = datetime.now() + relativedelta(days=3)
                    validate_date = validate_date.strftime("%d/%m/%Y")
                    validate_date = helper.validating_date(validate_date)
                    if (picking_date < validate_date):
                        messages.warning(self.request, "date are not right")
                        return redirect("main:checkout")
                    delivery_date = picking_date - timedelta(days=2)
                    due_date = helper.modify_due_date(delivery_date)
                    date = helper.get_picking_date_in_str(picking_date)
                else:
                    messages.warning(self.request, "Valitse noutopäivä")
                    return redirect("main:checkout")

                delivery = req.get('delivery')
                refrence = str(REFRENCE_LIST[0])
                print(refrence)
                REFRENCE_LIST.pop(0)
                helper.send_email_if_reference_number_list_empty(REFRENCE_LIST, settings.EMAIL_HOST_USER, "bassamalasadi@gmail.com")
                if req.get('deliver') != 0 or req.get('delivery') != 1:
                    amount = float(amount) + \
                        float(req.get('delivery'))
                amount = "{:.2f}".format(amount)
                deliv = 'Toimitus : ' + delivery + ' EURO' if float(delivery) > 0 else f''

                if helper.is_valid_form([firstName, lastName, phone, email, date, pay]):
                    order_list = helper.queryset_to_list(list(order_item))
                    order_email = helper.order_list_for_email(order_item)
                    req_order = Request.objects.create(
                        name=firstName,
                        address=address,
                        phone=phone,
                        email=email,
                        order=order_list,
                        create=datetime.now(),
                        delivery=picking_date,
                        delivery_price=delivery,
                    )
                    req_order_id = req_order.id
                    invoice_dict = {
                        'refrence':refrence,
                        'amount':amount,
                        'due_date': due_date
                    }

                    if payment_option == 'Invoice':
                        pay = helper.get_invoice_option(**invoice_dict)
                        pay_method = 'Lasku'
                    else:
                        pay = 'Maksu käteisellä tai Mobile Paylla (040 5177444) tilauksen toimituksen/noudon yhteydessä.'
                        pay_method = 'Käteinen / MobilePay'
                        due_date = f'{date}'

                    with open(f'{firstName} {lastName}.svg', 'wb') as f:
                        Code39(f'{refrence}', writer=ImageWriter()).write(f)
                    # create pdf invoice
                    create_invoice(
                        pay_date=due_date,
                        user_id=user.id,
                        lasku_id=req_order_id,
                        fname=firstName,
                        lname= lastName,
                        address=address,
                        postal=postal,
                        email=email,
                        store=order_email,
                        total=amount,
                        refrence=refrence,
                        delivery_way=delivery,
                        pay=pay,
                        pay_method=pay_method,
                    )
                    html_dict = {
                        'req_order': req_order_id,
                        'date': date,
                        'address': address,
                        'email': email,
                        'order_email': order_email,
                        'deliv': deliv,
                        'amount': amount,
                        'pay': pay,
                    }
                    subject = f'Tervetuloa {firstName} {lastName} Maisamin Herkkuun'
                    text_content = f"Moi, {lastName}"
                    html_content = helper.html_response_invoice(**html_dict)
                    email_to_us = EmailMultiAlternatives(
                        subject, text_content, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER, email],
                    )
                    email_to_us.attach_alternative(html_content, "text/html")
                    email_to_us.attach_file(f'{firstName} {lastName}.pdf')
                    email_to_us.send(fail_silently=False)

                    try:
                        os.remove(f'{firstName} {lastName}.pdf')
                        os.remove(f'{firstName} {lastName}.svg')
                        OrderItem.objects.filter(user=self.request.user).delete()
                    except:
                        HttpResponseBadRequest()
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
    paginate_by = 20
    template_name = "home.html"


class CakeView(ListView):
    paginate_by = 20
    template_name = "cake.html"

    def get_queryset(self):
        return Product.objects.filter(category='Kakut')

class CupcakeView(ListView):
    paginate_by = 20
    template_name = "cupcake.html"

    def get_queryset(self):
        return Product.objects.filter(category='Kuppikakut')

class CheeseCakeView(ListView):
    paginate_by = 20
    template_name = "cheesecake.html"

    def get_queryset(self):
        return Product.objects.filter(category='Juustokakut')


class FatayerView(ListView):
    paginate_by = 20
    template_name = "fatayer.html"

    def get_queryset(self):
        return Product.objects.filter(category='Fatayer')


class ManakishView(ListView):
    paginate_by = 20
    template_name = "manakish.html"

    def get_queryset(self):
        return Product.objects.filter(category='Manakish')


class MezeView(ListView):
    paginate_by = 20
    template_name = "meze.html"

    def get_queryset(self):
        return Product.objects.filter(category='Alkuruoat')


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order_item = OrderItem.objects.filter(user=self.request.user)
            num_entities = Product.objects.all().count()
            rand_entities = random.sample(range(1, num_entities), 2)
            sample_entities = Product.objects.filter(id__in=rand_entities)
            total = 0
            for order in order_item:
                total += float(order.get_final_price)
            total = "{:.2f}".format(total)
            context = {
                'object': total,
                'product': order_item,
                'sample':sample_entities,
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
                        if len(username) >= 3:
                            user.username = username
                            user.email = email
                            user.save()
                            messages.success(
                                self.request, "Muutokset tallennettu")
                            return redirect("main:profile")
                        else:
                            messages.success(
                                self.request, "Käyttäjätunnuksen tulee olla vähintään kolme kirjainta")
                            return redirect("main:profile")
                    except:
                        messages.success(
                            self.request, "Käyttäjätunnus tai sähköpostiosoite on varattu.")
                        return redirect("main:profile")

                else:
                    messages.warning(
                        self.request, "Käyttäjän tietoja ei muutettu.")
                return redirect("main:profile")
            if 'delete' in request.POST:
                delete = request.POST.get('deleteaccount')
                if (delete == 'poista'):
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
                else:
                    messages.warning(
                        self.request, 'Kirjoita " poista " ja napsauta sitten Poista tilisi -painiketta.')
                    return redirect("main:profile")

class ClientOrder(LoginRequiredMixin,
                  SuperUserCheck,
                  ListView):
    paginate_by = 20
    template_name = "clientorder.html"

    def get_queryset(self):
        return Request.objects.filter(delivery__gt=datetime.now())


class OrderDetail(LoginRequiredMixin,
                  SuperUserCheck,
                  DetailView):
    model = Request
    paginate_by = 20
    template_name = "order_detail.html"


class ItemDetailView(View):

    def get(self, *args, **kwargs):
        try:
            product = get_object_or_404(Product, slug=kwargs['slug'])
            num_entities = Product.objects.all().count()
            rand_entities = random.sample(range(1, num_entities), 3)
            sample_entities = Product.objects.filter(id__in=rand_entities)
            context = {
                'product': product,
                'sample':sample_entities,
            }
            return render(self.request, "product.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "not working")
            return redirect("main:home")

    def post(self, request, slug):
        add_info = ""
        if request.user.is_anonymous:
            return redirect('account_login')
        else:
            if request.POST.get('hinta-2'):
                price = sanitize_separators(request.POST.get('hinta-2'))
                amount = sanitize_separators(request.POST.get('amount-2'))
                gluteen = False
                laktoos = False
                add_info = sanitize_separators(request.POST.get('lisaa-2'))
            else:
                price = sanitize_separators(request.POST.get('price'))
                amount = sanitize_separators(request.POST.get('amount'))
                gluteen = sanitize_separators(request.POST.get('gluteen'))
                laktoos = sanitize_separators(request.POST.get('laktoos'))
                add_info = sanitize_separators(request.POST.get('lisaa'))
            if gluteen:
                price = str(float(price) + 9.00)
            if laktoos:
                price = str(float(price) + 5.00)

            product = get_object_or_404(Product, slug=slug)
            try:
                order_qs = OrderItem.objects.get(
                    user=self.request.user,
                    ordered=False,
                    product=product,
                    price=price,
                    is_gluteen_free=isinstance(gluteen ,str),
                    is_loctose_free=isinstance(laktoos ,str),
                    additional_info=add_info,
                    )
                order_qs.quantity += int(amount)

                if gluteen:
                    order_qs.is_gluteen_free = True
                if laktoos:
                    order_qs.is_loctose_free = True
                order_qs.save()
                messages.info(
                    self.request, "Tämä tuote lisättiin ostoskoriin")
                return redirect("main:product", slug=slug)
            except OrderItem.DoesNotExist:
                OrderItem.objects.create(
                    product=product,
                    user=request.user,
                    ordered=False,
                    price=price,
                    quantity=amount,
                    is_gluteen_free=isinstance(gluteen ,str),
                    is_loctose_free=isinstance(laktoos ,str),
                    additional_info=add_info,
                )
                messages.info(
                    self.request, "Tämä tuote lisättiin ostoskoriin")
                return redirect("main:product", slug=slug)
            except:
                 HttpResponseBadRequest()


@ login_required
def add_to_cart(request, slug, **kwargs):
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
def remove_from_cart(request, pk):
    try:
        product = get_object_or_404(OrderItem, pk=pk)
        product.delete()
        messages.info(request, "Tämä tuote poistettiin ostoskorista")
        return redirect("main:order-summary")
    except:
        messages.info(request, "Tätä tuotetta ei ollut ostoskorissa")
        return redirect("main:order-summary")



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

class Delivery(View):
    def get(self, *args, **kwargs):
        return render(self.request, "delivery_policy.html")

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        redirect_to = request.GET.get('next', '')
        return HttpResponseRedirect(redirect_to)


def delete_model(request, pk):
    item = get_object_or_404(OrderItem, id=pk)
    if item:
        ref = item.id
        item.delete()
        data = {'ref': ref, 'message': 'Object with id %s has been deleted' %ref}
        return JsonResponse(data)

def increment(request, pk):
    item = get_object_or_404(OrderItem, id=pk)
    if item:
        ref = item.id
        item.quantity += 1
        item.save()
        data = {'ref': ref, 'message': 'Object with id %s has been update' %ref}
        return JsonResponse(data)

def decrement(request, pk):
    item = get_object_or_404(OrderItem, id=pk)
    if item:
        ref = item.id
        item.quantity -= 1
        item.save()
        data = {'ref': ref, 'message': 'Object with id %s has been update' %ref}
        return JsonResponse(data)
