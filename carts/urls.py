from django.urls import path

from carts.views import (
    cart_view,
    add_to_cart,
    cart_item_delete,
    checkbox_check,
    delete_order,
    recent_order,
    list_of_orders,
    detail_order,
    delete_order
)



app_name="carts"
urlpatterns = [

    path('', cart_view, name="cart"),
    path('add-to-cart/<int:pk>/', add_to_cart, name="add_to_cart"),
    path('checkout/', checkbox_check, name="checkout"),
    path('recent-order/', recent_order, name="recent_order"),
    path('orders/', list_of_orders, name='orders'),
    path('order-detail/<int:pk>/', detail_order, name="detail_order")
]

htmx_urlpatterns = [
    path('cart-item-delete/<int:pk>/', cart_item_delete, name="cart_item_delete"),
    path('delete-order/<int:pk>/', delete_order, name="delete_order")
]

urlpatterns += htmx_urlpatterns