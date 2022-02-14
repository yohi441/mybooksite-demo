from django.urls import resolve, reverse




def test_cart_url():
    path = reverse('carts:cart')
    assert resolve(path).view_name == 'carts:cart'


def test_cart_add_to_cart_url():
    path = reverse('carts:add_to_cart', kwargs={'pk': 1})
    assert resolve(path).view_name == 'carts:add_to_cart'


def test_cart_item_delete_url():
    path = reverse('carts:cart_item_delete', kwargs={'pk':1})
    assert resolve(path).view_name == 'carts:cart_item_delete'


def test_checkout_url():
    path = reverse('carts:checkout')
    assert resolve(path).view_name == 'carts:checkout'

def test_recent_order_url():
    path = reverse('carts:recent_order')
    assert resolve(path).view_name == 'carts:recent_order'

def test_orders_url():
    path = reverse('carts:orders')
    assert resolve(path).view_name == 'carts:orders'

def test_detail_order_url():
    path = reverse('carts:detail_order', kwargs={'pk':1})
    assert resolve(path).view_name == 'carts:detail_order'

def test_delete_order_url():
    path = reverse('carts:delete_order', kwargs={'pk':1})
    assert resolve(path).view_name == 'carts:delete_order'


