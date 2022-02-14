from tabnanny import check
from django.contrib.auth.models import User
from carts.models import Cart, Checkout
from mybooksite.models import Book
import pytest





@pytest.mark.django_db
def test_create_cart():
    user = User.objects.create(username="testusername", password="testpassword")
    
    count = Cart.objects.all().count()

    book_count = user.cart.books.all().count()
    

    assert count == 1
    assert book_count == 0

@pytest.mark.django_db
def test_update_cart():
    user = User.objects.create(username="testusername", password="testpassword")

    book = Book.objects.create(title="booktitle", price=123.00, rating=3, description="book description")

    user.cart.books.add(book)

    assert user.cart.books.all().count() == 1
    assert user.cart.books.all()[0].title == 'booktitle'
    assert user.cart.books.all()[0].price == 123.00
    assert user.cart.books.all()[0].rating == 3
    assert user.cart.books.all()[0].description == 'book description'


@pytest.mark.django_db
def test_remove_item_cart():
    user = User.objects.create(username="testusername", password="testpassword")

    book = Book.objects.create(title="booktitle", price=123.00, rating=3, description="book description")
    user.cart.books.add(book)
    
    assert user.cart.books.all().count() == 1
    user.cart.books.remove(book)
    assert user.cart.books.all().count() == 0


@pytest.mark.django_db
def test_create_checkout():
    user = User.objects.create(username="testusername", password="testpassword")

    Checkout.objects.create(user=user)

    count = Checkout.objects.all().count()

    assert count == 1


@pytest.mark.django_db
def test_update_checkout():
    user = User.objects.create(username="testusername", password="testpassword")

    book = Book.objects.create(title="booktitle", price=123.00, rating=3, description="book description")

    checkout = Checkout.objects.create(user=user)

    checkout.books.add(book)

    assert checkout.books.all().count() == 1


@pytest.mark.django_db
def test_delete_item_checkout():
    user = User.objects.create(username="testusername", password="testpassword")

    book = Book.objects.create(title="booktitle", price=123.00, rating=3, description="book description")

    checkout = Checkout.objects.create(user=user)

    checkout.books.add(book)
    assert checkout.books.all().count() == 1
    checkout.books.remove(book)
    assert checkout.books.all().count() == 0


    

    

    

   


    
