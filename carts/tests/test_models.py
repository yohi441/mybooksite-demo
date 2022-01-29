from django.contrib.auth.models import User
from carts.models import Cart
import pytest





@pytest.mark.django_db
def test_create_user():
    User.objects.create(username="testusername", password="testpassword")
    count = User.objects.all().count()
    user = User.objects.get(pk=1)
    assert user.cart.total == 0.0
    assert count == 1
    assert user.username == "testusername"
    assert user.password == "testpassword"


   


    
