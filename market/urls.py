from django.urls import path
from .views import MarketListView, MarketDetailView, MarketCreateView, \
    MarketUpdateView, MarketDeleteView


urlpatterns = [
    path('', MarketListView.as_view(), name='market_list'),
    path('new/', MarketCreateView.as_view(), name='market_create'),
    path('<int:pk>/', MarketDetailView.as_view(), name='market_detail'),
    path('<int:pk>/update/', MarketUpdateView.as_view(), name='market_update'),
    path('<int:pk>/delete/', MarketDeleteView.as_view(), name='market_delete'),
]
