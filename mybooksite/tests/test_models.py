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
    


@pytest.fixture()
def book(request, db):
    return mixer.blend('mybooksite.Book', quantity=request.param)


@pytest.mark.parametrize('book',[1], indirect=True)
def test_book_is_in_stock(book):
    assert book.is_in_stock == 'in stock'


@pytest.mark.parametrize('book',[0], indirect=True)
def test_book_is_out_of_stock(book):
    assert book.is_in_stock == 'out of stock'