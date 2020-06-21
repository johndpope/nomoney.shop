from django.urls import path
from bid.views import BidOverView, BidListView, BidCreateView, BidDetailView, BidDeleteView
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', BidOverView.as_view(), name='bid_overview'),
    path('partner/<int:partner_pk>/', BidListView.as_view(), name='bid_list'),
    path('partner/<int:partner_pk>/new/', BidCreateView.as_view(), name='bid_create'),
    path('<int:pk>/', BidDetailView.as_view(), name='bid_detail'),
    path('<int:bid_pk>/delete/', BidDeleteView.as_view(), name='bid_delete'),
]

