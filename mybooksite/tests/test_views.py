from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from mybooksite.views import detail_view
from mixer.backend.django import mixer
from django.contrib.sessions.middleware import SessionMiddleware
import pytest


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()

@pytest.fixture()
def book(db):
    return mixer.blend('mybooksite.Book')

def test_detail_view(factory, book):
    path = reverse('mybooksite:detail', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = AnonymousUser() 

    def dummy_get_response(request):
        return None

    SessionMiddleware(dummy_get_response).process_request(request)
    request.session.save()
    response = detail_view(request, pk=1)
    assert response.status_code == 200
