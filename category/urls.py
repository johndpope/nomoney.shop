""" urls for the category module """
from django.urls import path
from .views import CategoryListView, CategoryCreateView, CategoryDetailView, \
    CategoryUpdateView, CategoryAjaxView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('new/', CategoryCreateView.as_view(), name='category_create'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('ajax/<int:pk>/', CategoryAjaxView.as_view(), name='category_details_ajax'),
]
