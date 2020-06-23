from django.urls import path
from .views import DealCreateView, DealDetailView, DealListView, DealUpdateView

urlpatterns = [
    path('', DealListView.as_view(), name='deal_list'),
    path('new/', DealCreateView.as_view(), name='deal_create'),
    path('<int:pk>/', DealDetailView.as_view(), name='deal_detail'),
    path('<int:pk>/update', DealUpdateView.as_view(), name='deal_update'),
]
