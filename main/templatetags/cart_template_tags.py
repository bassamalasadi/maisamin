from django import template
from main.models import Order, OrderItem
register = template.Library()

# counting the number of orders in your navbar cart


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = OrderItem.objects.filter(user=user)
        if qs.exists():
            return qs.count()
    return 0
