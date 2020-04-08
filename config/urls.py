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
from home.views import Home
from listing.views import ListingListView, ListingDetailView, ListingCreateView, ListingUpdateView, ListingDeleteView
from user.views import CalculatorView, PushView, PullView

urlpatterns = [
    #path('', Home.as_view(), name='home'),

    path('calc/', CalculatorView.as_view(), name='calculator'),
    path('push/', PushView.as_view(), name='push'),
    path('pull/', PullView.as_view(), name='pull'),

    path('', ListingListView.as_view(), name='listing-list'),
    path('listing/', ListingListView.as_view(), name='listing-list'),
    path('listing/create/', ListingCreateView.as_view(), name='listing-create'),
    path('listing/<int:pk>/update', ListingUpdateView.as_view(), name='listing-update'),
    path('listing/<int:pk>/delete', ListingDeleteView.as_view(), name='listing-delete'),
    path('listing/<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
    path('admin/', admin.site.urls),
]
