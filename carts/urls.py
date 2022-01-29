from django.urls import path

from carts.views import (
    cart_view,
    add_to_cart,
    cart_item_delete
)



app_name="carts"
urlpatterns = [

    path('<int:pk>/', cart_view, name="cart"),
    path('add-to-cart/<int:pk>/', add_to_cart, name="add_to_cart"),
]

htmx_urlpatterns = [
    path('cart-item-delete/<int:pk>/', cart_item_delete, name="cart_item_delete"),
]

urlpatterns += htmx_urlpatterns