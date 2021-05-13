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
from .models import Product, OrderItem, Order, Request
from .lasku import create_invoice


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
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


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
            messages.info(self.request, _("You do not have an active order"))
            return redirect("main:home")

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        pay = 'You will pay when the order deliverd or picked up'
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
                date = datetime(year, month, day) - timedelta(days=1)
                delivery = req.get('delivery')
                if req.get('deliver') != 0 or req.get('delivery') != 1:
                    amount = float(order_item.get_total()) + \
                        float(req.get('delivery'))
                if req.get('payment_option') == 'Invoice':
                    pay = f"""
                        Payee's IBAN :   \n
                        Payment Reference:  \n
                        Amount: {amount} \n
                        Due date :
                    """

                if is_valid_form([firstName, lastName, city, street_address,
                                  postal, phone, email, delivery,
                                  date, pay]):
                    order_list = queryset_to_list(
                        list(order_item.products.all()))
                    Request.objects.create(
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
                        delivery_date=date.strftime('%Y-%m-%d'),
                        name=firstName + lastName,
                        address=address,
                        email=email,
                        store=product_order,
                        totel=amount,
                        delivery_way=delivery,
                    )
                    subject = f'Welcome {firstName} {lastName} to Maysam Cake Shop'
                    message = f""" Moi, {lastName}  \n
Your order request code{order_item.id} will be delivered in 72 hours {str(order_item.create)[0:16]} to your home address: {address} \n
Your order: \n
{order_list} \n

Thank you to choosing Maysam Cake Shop if You want to cancel your order send request order code : {order_item.id}  to this number (0403232323)
or to this email (tmren613@gmail.com) \n
{pay}
Thank you

                    """

                    recepient = email
                    email = EmailMessage(
                        subject, message, settings.EMAIL_HOST_USER, [
                            recepient, settings.EMAIL_HOST_USER]
                    )
                    email.attach_file(f'{firstName}{lastName}.pdf')
                    email.send()
                    OrderItem.objects.filter(user=self.request.user).delete()
            else:
                messages.warning(self.request, "Invalid form")
                return redirect("main:checkout")
            context = {
                'form': form
            }
            return render(self.request, "message.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
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
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(
                self.request, "You do not have an active order")
            return redirect("/")


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

        product = get_object_or_404(Product, slug=slug)
        if request.user.is_anonymous:
            return redirect('account_login')
        else:
            try:
                order_product, created = OrderItem.objects.get_or_create(
                    product=product,
                    user=self.request.user,
                    ordered=False,
                    price=price
                )
                order_qs = Order.objects.filter(
                    user=self.request.user, ordered=False)

                if order_qs.exists():
                    order = order_qs[0]
                    # check if the order item is in the order
                    if order.products.filter(product__slug=product.slug, price=price).exists():
                        order_product.quantity += 1
                        order_product.save()
                        messages.info(
                            self.request, "This product quantity was updated.")
                        return redirect("main:order-summary")
                    else:
                        order.products.add(order_product)
                        messages.info(
                            self.request, "This product was added to your cart.")
                        return redirect("main:order-summary")
                else:
                    order = Order.objects.create(
                        user=self.request.user)
                    order.products.add(order_product)
                    messages.info(
                        self.request, "This product was added to your cart.")
                    return redirect("main:order-summary")
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
            messages.info(request, "This product quantity was updated.")
            return redirect("main:order-summary")

        else:
            order.products.add(order_product)
            messages.info(request, "This product was added to your cart.")
            return redirect("main:order-summary")
    else:
        order = Order.objects.create(
            user=request.user)
        order.products.add(order_product)
        messages.info(request, "This product was added to your cart.")
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
            messages.info(request, "This product quantity was updated.")
            return redirect("main:order-summary")
        else:
            messages.info(request, "This product was not in your cart")
            return redirect("main:order-summary")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("main:order-summary")


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
            messages.info(request, "This product was removed from your cart.")
            return redirect("main:order-summary")
        else:
            messages.info(request, "This product was not in your cart")
            return redirect("main:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("main:product", slug=slug)


@ user_passes_test(lambda u: u.is_superuser)
def remove_from_order_page(request, pk):
    order = get_object_or_404(Request, pk=pk)
    if order:
        order.delete()
        messages.info(request, 'This product has been delete')
        return redirect("main:client-order")
    else:
        messages.info(request, 'You have no request to delete')
        return redirect("main:client-order")
