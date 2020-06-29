from django.urls import path
from .views import DealCreateView, DealDetailView, DealListView, DealUserCreateView, DealAcceptedView

urlpatterns = [
    path('', DealListView.as_view(), name='deal_list'),
    path('<int:pk>/', DealDetailView.as_view(), name='deal_detail'),
    path('<int:pk>/accept/', DealAcceptedView.as_view(), name='deal_accepted'),
    path('create/', DealCreateView.as_view(), name='deal_create'),
    path(
        'create/<int:partner_pk>/',
        DealUserCreateView.as_view(),
        name='deal_user_create'
        ),
]
