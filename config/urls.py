"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from listing.views import ListingListView, ListingDetailView, \
    ListingCreateView, ListingUpdateView, ListingDeleteView
from user.views import UserListView, UserCreateView, UserUpdateView, UserDetailView, AgentView
from bid.views import BidOverView, BidListView, BidCreateView, BidDetailView, BidDeleteView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home/home.html'), name='home'),

    path('list/', ListingListView.as_view(), name='listing_list'),
    path('list/<slug:type>/new/', ListingCreateView.as_view(), name='listing_create'),
    path('list/<slug:type>/<int:pk>/', ListingDetailView.as_view(), name='listing_detail'),
    path('list/<slug:type>/<int:category_id>/new/', ListingCreateView.as_view(), name='listing_create'),
    path('list/<slug:type>/<int:pk>/update/', ListingUpdateView.as_view(), name='listing_update'),
    path('list/<slug:type>/<int:pk>/delete', ListingDeleteView.as_view(), name='listing_delete'),

    path('bid/', BidOverView.as_view(), name='bid_overview'),
    path('bid/partner/<int:partner_pk>/', BidListView.as_view(), name='bid_list'),
    path('bid/partner/<int:partner_pk>/new/', BidCreateView.as_view(), name='bid_create'),
    path('bid/<int:pk>/', BidDetailView.as_view(), name='bid_detail'),
    path('bid/<int:bid_pk>/delete/', BidDeleteView.as_view(), name='bid_delete'),

    path('agent/', AgentView.as_view(), name='agent_list'),

    path('user/', UserListView.as_view(), name='user_list'),
    path('user/new/', UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/pw/', PasswordChangeView.as_view(template_name='user/user_form.html'), name='user_pw'),
    path('user/login/', LoginView.as_view(template_name='user/user_form.html'), name='user_login'),
    path('user/logout/', LogoutView.as_view(), name='user_logout'),

    path('admin/', admin.site.urls),
]

