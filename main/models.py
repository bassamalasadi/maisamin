# define the logic and the order such as adding and removing items from cart

from django.conf import settings
from django.db import models
from django.db.models.fields import DecimalField
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
SIZE = (
    ('6 People', '6 People'),
    ('8 People', '8 People'),
    ('12 People', '12 People'),
    ('16 People', '16 People'),
    ('20 People', '20 People')
)

CATEGORY = (
    ('cake', 'cake'),
    ('pastry', 'pastry'),
    ('cheesecake', 'cheesecake'),
    ('manakish', 'manakish'),
    ('meze', 'meze'),
    ('cupcake', 'cupcake'),
)

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    category = models.CharField(choices=CATEGORY, max_length=20)
    contents = models.TextField(null=True, blank=True)
    is_gluteen_free = models.BooleanField(default=False)
    is_loctose_free = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField()
    image1 = models.TextField(null=True, blank=True)
    size = MultiSelectField(choices=SIZE)

    def __str__(self):
        return self.name

    # Get the product by it's Slug
    def get_absolute_url(self):
        return reverse("main:product", kwargs={'slug': self.slug})

    # Adding product to the cart in: templates/product.html
    # using function in main/view.py
    def get_add_to_cart_url(self):
        return reverse("main:add-to-cart", kwargs={'slug': self.slug})

    # remove product from order list in : templates/order_summary.html
    # using function in main/views.py

    def get_remove_from_cart_url(self):
        return reverse("main:remove-from-cart", kwargs={'slug': self.slug})

# client add product to the cart


class OrderItem(models.Model):
    # user data
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # number of order that render in cart
    ordered = models.BooleanField(default=False)
    # the product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # the products' quantity
    quantity = models.IntegerField(default=1)
    # size of the product
    price = models.DecimalField(max_digits=10, decimal_places=2)

    is_gluteen_free = models.BooleanField(default=False)
    is_loctose_free = models.BooleanField(default=False)

    additional_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} : qunatity = ({self.quantity}) : price = ({self.price}) : is_G = ({self.is_gluteen_free}) : is_L = ({self.is_loctose_free}) : add_info=({self.additional_info})"

    # to calculate the sum of the price for a specified quantity for a single product
    @property
    def get_total_product_price(self):
        return float(self.quantity * self.price)

    # to get the prices of the total product if has a discount on it or no
    @property
    def get_final_price(self):
        print(self.get_total_product_price)
        print("{:.2f}".format(self.get_total_product_price))
        return "{:.2f}".format(self.get_total_product_price)

    @property
    def get_product(self):
        return self.product.name

    @property
    def get_quantity(self):
        return self.quantity

    @property
    def get_item_detail(self):
        return [self.get_product, self.get_quantity, self.get_total_product_price, self.is_gluteen_free, self.is_loctose_free]

    def is_ordered(self):
        if self.ordered:
            return True


# handle all the order data
# To calculate all final prices and saving for the order

class Order(models.Model):
    # user data
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # the products
    products = models.ManyToManyField(OrderItem)
    # number of order
    ordered = models.BooleanField(default=False)
    # size of the product
    create = models.DateTimeField(auto_now_add=True)
    # dunder method that get the user name

    def __str__(self):
        return self.user.username

    # The function will calculate the overall  prices for all products in : templates/order_summary.html
    @property
    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price
        return total

    @property
    def get_items_detail(self):
        prod_list = []
        for order_product in self.products.all():
            prod_list.append(order_product.get_item_detail)
        return prod_list


class Address(models.Model):
    firstName = models.CharField(max_length=100, blank=False, null=False)
    lastName = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    street_address = models.CharField(max_length=100, blank=False, null=False)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    postal = models.CharField(max_length=100, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(max_length=200, blank=False, null=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.firstName

    class Meta:
        verbose_name_plural = 'Addresses'


class Request(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    order = models.TextField()
    create = models.DateTimeField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    delivery = models.DateTimeField()
    delivery_price = models.CharField(max_length=10)

    def __str__(self):
        return str(self.create)

    def get_absolute_url(self):
        return reverse("main:order-detail", kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-id']


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.product} {self.size}'
