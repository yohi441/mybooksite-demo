from mixer.backend.django import mixer
from mybooksite.models import Book
import pytest


@pytest.mark.django_db
def test_book_create():
    Book.objects.create(title="booktitle", price=123.00, rating=3, description="book description")
    count = Book.objects.all().count()
    book = Book.objects.get(pk=1)
    assert book.title == "booktitle"
    assert book.price == 123.00
    assert book.rating == 3
    assert book.description == "book description"
    assert book.quantity == 1
    assert count == 1

@pytest.mark.django_db
def test_book_update():
    Book.objects.create(title="booktitle", price=123.00, rating=3, description="book description")
    book = Book.objects.get(pk=1)

    book.title = "bookupdated"
    book.price = 125.00
    book.rating = 5
    book.description = "book description updated"
    book.quantity = 5

    assert book.title == "bookupdated"
    assert book.price == 125.00
    assert book.rating == 5
    assert book.description == "book description updated"
    assert book.quantity == 5


@pytest.mark.django_db
def test_book_delete():
    Book.objects.create(title="booktitle", price=123.00, rating=3, description="book description")
    book = Book.objects.get(pk=1)

    assert Book.objects.all().count() == 1

    book.delete()
    
    count = Book.objects.all().count()

    assert count == 0


@pytest.fixture()
def book(request, db):
    return mixer.blend('mybooksite.Book', quantity=request.param)


@pytest.mark.parametrize('book',[1], indirect=True)
def test_book_is_in_stock(book):
    assert book.is_in_stock == 'in stock'


@pytest.mark.parametrize('book',[0], indirect=True)
def test_book_is_out_of_stock(book):
    assert book.is_in_stock == 'out of stock'