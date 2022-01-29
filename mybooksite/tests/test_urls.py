from django.urls import resolve, reverse
import pytest

@pytest.mark.parametrize('param', [
    'mybooksite:index',
    'mybooksite:search',   
    'mybooksite:about_us',
])

def test_mybooksite_urls(param):
    path = reverse(param)
    print(path)
    assert resolve(path).view_name == param

def test_book_detail_url():
    path = reverse('mybooksite:detail', kwargs={'pk': 1})
    assert resolve(path).view_name == 'mybooksite:detail'

def test_category_url():
    path = reverse('mybooksite:category', kwargs={'pk': 1})
    assert resolve(path).view_name == 'mybooksite:category'
    


