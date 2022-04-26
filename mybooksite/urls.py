from django.urls import path

from .views import BookDetailView, IndexView, AboutUsView, SearchView, CategoryView


app_name = "mybooksite"
urlpatterns = [
    
    path('', IndexView.as_view(), name="index"),
    path('search/', SearchView.as_view(), name='search'),
    path('book-detail/<int:pk>', BookDetailView.as_view(), name="detail"),
    path('category/<int:pk>', CategoryView.as_view(), name='category'),
    path('about-us/', AboutUsView.as_view(), name="about_us"),
    
]




