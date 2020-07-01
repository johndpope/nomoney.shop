from django.urls import path
from .views import SearchView, AjaxPollView


urlpatterns = [
    path('', SearchView.as_view(), name='search_basic'),
    path('advanced', SearchView.as_view(), name='search_advanced'),
    path('ajax/live/<slug:search_string>/', AjaxPollView.as_view(), name='search_advanced'),
]
