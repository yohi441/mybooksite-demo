from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import Http404
from mybooksite.views import IndexView, BookDetailView, AboutUsView, SearchView, CategoryView
from mybooksite.models import Book, Category
from mixer.backend.django import mixer
import pytest


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def book(db):
    return mixer.blend('mybooksite.Book')


@pytest.fixture
def category(db):
    return mixer.blend('mybooksite.Category')


def _add_session(request):
    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session.save()


@pytest.mark.django_db
class TestIndexView:

    def test_status_code(self, factory):
        request = factory.get(reverse('mybooksite:index'))
        request.user = AnonymousUser()
        _add_session(request)
        response = IndexView.as_view()(request)
        assert response.status_code == 200

    def test_template(self, factory):
        request = factory.get(reverse('mybooksite:index'))
        request.user = AnonymousUser()
        _add_session(request)
        response = IndexView.as_view()(request)
        assert 'index.html' in response.template_name

    def test_context_contains_categories(self, factory, category):
        request = factory.get(reverse('mybooksite:index'))
        request.user = AnonymousUser()
        _add_session(request)
        response = IndexView.as_view()(request)
        assert 'categories' in response.context_data


@pytest.mark.django_db
class TestBookDetailView:

    def test_status_code(self, factory, book):
        request = factory.get(reverse('mybooksite:detail', kwargs={'pk': book.pk}))
        request.user = AnonymousUser()
        _add_session(request)
        response = BookDetailView.as_view()(request, pk=book.pk)
        assert response.status_code == 200

    def test_context_contains_book(self, factory, book):
        request = factory.get(reverse('mybooksite:detail', kwargs={'pk': book.pk}))
        request.user = AnonymousUser()
        _add_session(request)
        response = BookDetailView.as_view()(request, pk=book.pk)
        assert response.context_data['book'] == book

    def test_template(self, factory, book):
        request = factory.get(reverse('mybooksite:detail', kwargs={'pk': book.pk}))
        request.user = AnonymousUser()
        _add_session(request)
        response = BookDetailView.as_view()(request, pk=book.pk)
        assert response.template_name[0] == 'detail.html'

    def test_404_for_invalid_pk(self, factory):
        request = factory.get(reverse('mybooksite:detail', kwargs={'pk': 999}))
        request.user = AnonymousUser()
        _add_session(request)
        with pytest.raises(Http404):
            BookDetailView.as_view()(request, pk=999)


@pytest.mark.django_db
class TestCategoryView:

    def test_status_code(self, factory, category):
        request = factory.get(reverse('mybooksite:category', kwargs={'pk': category.pk}))
        request.user = AnonymousUser()
        _add_session(request)
        response = CategoryView.as_view()(request, pk=category.pk)
        assert response.status_code == 200

    def test_context_contains_categories(self, client, category):
        response = client.get(reverse('mybooksite:category', kwargs={'pk': category.pk}))
        assert response.status_code == 200
        assert 'categories' in response.context

    def test_context_contains_page_obj(self, client, category):
        response = client.get(reverse('mybooksite:category', kwargs={'pk': category.pk}))
        assert 'page_obj' in response.context


@pytest.mark.django_db
class TestAboutUsView:

    def test_status_code(self, factory):
        request = factory.get(reverse('mybooksite:about_us'))
        request.user = AnonymousUser()
        _add_session(request)
        response = AboutUsView.as_view()(request)
        assert response.status_code == 200

    def test_template(self, factory):
        request = factory.get(reverse('mybooksite:about_us'))
        request.user = AnonymousUser()
        _add_session(request)
        response = AboutUsView.as_view()(request)
        assert 'about_us.html' in response.template_name


@pytest.mark.django_db
class TestSearchView:

    def test_status_code_with_query(self, factory, book):
        request = factory.get(reverse('mybooksite:search'), data={'q': book.title[:5]})
        request.user = AnonymousUser()
        _add_session(request)
        response = SearchView.as_view()(request)
        assert response.status_code == 200

    def test_returns_books_matching_query(self, client, book):
        response = client.get(reverse('mybooksite:search'), {'q': book.title[:5]})
        assert response.status_code == 200
        assert book in response.context['books']

    def test_empty_query_returns_none(self, client):
        response = client.get(reverse('mybooksite:search'), {'q': ''})
        assert response.context['books'] is None
