import io
import os
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from mixer.backend.django import mixer
from mybooksite.models import Book, Category
from PIL import Image
import pytest


def _make_test_image():
    img = Image.new('RGB', (1, 1))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return SimpleUploadedFile("test.jpg", buf.getvalue(), content_type="image/jpeg")


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
def test_book_str():
    book = Book.objects.create(title="booktitle", price=10.00, rating=3, description="desc")
    assert str(book) == "booktitle"


@pytest.mark.django_db
def test_book_rating_choices():
    book = Book.objects.create(title="booktitle", price=10.00, rating=3, description="desc")
    assert book.rating in [1, 2, 3, 4, 5]


@pytest.mark.django_db
def test_book_img_url_no_image():
    book = Book.objects.create(title="booktitle", price=10.00, rating=3, description="desc")
    assert "placeholder" in book.img_url


@pytest.mark.django_db
def test_book_img_url_blank_image():
    book = Book.objects.create(title="booktitle", price=10.00, rating=3, description="desc", img=None)
    assert "placeholder" in book.img_url


@override_settings(
    STORAGES={
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
    },
    MEDIA_ROOT=os.path.join(tempfile.mkdtemp(), 'media'),
)
@pytest.mark.django_db
def test_book_img_url_with_image():
    img = _make_test_image()
    book = Book.objects.create(title="booktitle", price=10.00, rating=3, description="desc", img=img)
    assert book.img_url == book.img.url
    assert "placeholder" not in book.img_url


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


@pytest.mark.parametrize('book', [1], indirect=True)
def test_book_is_in_stock(book):
    assert book.is_in_stock == 'in stock'


@pytest.mark.parametrize('book', [0], indirect=True)
def test_book_is_out_of_stock(book):
    assert book.is_in_stock == 'out of stock'


@pytest.mark.django_db
def test_category_create():
    category = Category.objects.create(name="Test Category")
    assert category.name == "Test Category"
    assert Category.objects.count() == 1


@pytest.mark.django_db
def test_category_str():
    category = Category.objects.create(name="Test Category")
    assert str(category) == "Test Category"


@pytest.mark.django_db
def test_category_verbose_name_plural():
    assert Category._meta.verbose_name_plural == "Categories"


@pytest.mark.django_db
def test_category_add_book():
    book = Book.objects.create(title="booktitle", price=10.00, rating=3, description="desc")
    category = Category.objects.create(name="Test Category")
    category.books.add(book)
    assert category.books.count() == 1
    assert book in category.books.all()


@pytest.mark.django_db
def test_category_remove_book():
    book = Book.objects.create(title="booktitle", price=10.00, rating=3, description="desc")
    category = Category.objects.create(name="Test Category")
    category.books.add(book)
    assert category.books.count() == 1
    category.books.remove(book)
    assert category.books.count() == 0
