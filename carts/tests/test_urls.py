from django.urls import resolve, reverse




def test_cart_url():
    path = reverse('carts:cart', kwargs={'pk': 1})
    assert resolve(path).view_name == 'carts:cart'




def test_cart_add_to_cart_url():
    path = reverse('carts:add_to_cart', kwargs={'pk': 1})
    assert resolve(path).view_name == 'carts:add_to_cart'




def test_cart_item_delete_url():
    path = reverse('carts:cart_item_delete', kwargs={'pk': 1})
    assert resolve(path).view_name == 'carts:cart_item_delete'