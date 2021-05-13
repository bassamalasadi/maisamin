from django.contrib import admin
from .models import Product, OrderItem, Order, Address, Request, Variation


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_display_links = ['user']


admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Variation)
admin.site.register(Address)
admin.site.register(Request)
