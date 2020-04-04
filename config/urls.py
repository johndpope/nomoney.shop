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
from action.views import ActionListView, ActionDetailView, ActionCreateView, ActionUpdateView, ActionDeleteView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('action/', ActionListView.as_view(), name='action-list'),
    path('action/create/', ActionCreateView.as_view(), name='action-create'),
    path('action/<int:pk>/update', ActionUpdateView.as_view(), name='action-update'),
    path('action/<int:pk>/delete', ActionDeleteView.as_view(), name='action-delete'),
    path('action/<int:pk>/', ActionDetailView.as_view(), name='action-detail'),
    path('admin/', admin.site.urls),
]
