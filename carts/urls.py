from django.urls import path

from carts.views import (
    cart_view,
    add_to_cart
)



app_name="carts"
urlpatterns = [

    path('carts/<int:pk>', cart_view, name="cart"),
    path('cart/<int:pk>', add_to_cart, name="add_to_cart"),
]