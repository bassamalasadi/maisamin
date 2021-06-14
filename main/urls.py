from django.urls import path, re_path
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    CakeView,
    CupcakeView,
    CheeseCakeView,
    FatayerView,
    ClientOrder,
    OrderDetail,
    ManakishView,
    MezeView,
    Privacy,
    Profile,
    add_to_cart,
    testView,
    remove_from_cart,
    remove_single_item_from_cart,
    remove_from_order_page,
)

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('test/', testView, name="test"),
    path('cake/', CakeView.as_view(), name='cake'),
    path('cupcake', CupcakeView.as_view(), name='cupcake'),
    path('cheesecake/', CheeseCakeView.as_view(), name='cheesecake'),
    path('fatayer', FatayerView.as_view(), name='fatayer'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('manakish/', ManakishView.as_view(), name='manakish'),
    path('meze/', MezeView.as_view(), name='meze'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('remove-from-cart/<pk>/', remove_from_cart, name='remove-from-cart'),

    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-to-cart/<slug>/<price>/', add_to_cart, name='add-to-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('remove-item-from-cart/<int:slug>/<price>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('clientorder/', ClientOrder.as_view(), name="client-order"),
    path('order-detail/<int:pk>/', OrderDetail.as_view(), name="order-detail"),
    path('remove_from_order_page/<int:pk>/',
         remove_from_order_page, name="remove_from_order_page"),
    path('privacy-policy/', Privacy.as_view(), name="privacy"),
    path('accounts/profile/', Profile.as_view(), name="profile")
]
