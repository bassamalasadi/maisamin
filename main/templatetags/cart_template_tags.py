from django import template
from main.models import Order

register = template.Library()

# counting the number of orders in your navbar cart


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].products.count()
    return 0
