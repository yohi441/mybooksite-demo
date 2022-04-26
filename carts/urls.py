from django.urls import path
from carts.views import (
    CheckboxCheck,
    CartView,
    AddToCart,
    CartItemDelete,
    DeleteOrder,
    RecentOrder,
    ListOfOrders,
    DetailOrder,
)



app_name="carts"
urlpatterns = [

    path('', CartView.as_view(), name="cart"),
    path('add-to-cart/<int:pk>/', AddToCart.as_view(), name="add_to_cart"),
    path('checkout/', CheckboxCheck.as_view(), name="checkout"),
    path('recent-order/', RecentOrder.as_view(), name="recent_order"),
    path('orders/', ListOfOrders.as_view(), name='orders'),
    path('order-detail/<int:pk>/', DetailOrder.as_view(), name="detail_order")
]

htmx_urlpatterns = [
    path('cart-item-delete/<int:pk>/', CartItemDelete.as_view(), name="cart_item_delete"),
    path('delete-order/<int:pk>/', DeleteOrder.as_view(), name="delete_order")
]

urlpatterns += htmx_urlpatterns