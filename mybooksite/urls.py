from django.urls import path

from .views import (
    index_view,
    about_us_view,
    detail_view,
    search_view,
    category_view
)

app_name = "mybooksite"
urlpatterns = [
    path('', index_view, name="index"),
    path('search/', search_view, name='search'),
    path('book-detail/<int:pk>', detail_view, name="detail"),
    path('category/<int:pk>', category_view, name='category'),
    path('about-us/', about_us_view, name="about_us"),     
]
