from django.urls import path
from .views import SearchView


urlpatterns = [
    path('', SearchView.as_view(), name='search_basic'),
    path('advanced', SearchView.as_view(), name='search_advanced'),
]