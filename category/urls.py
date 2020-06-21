from django.urls import path
from .views import CategoryListView, CategoryCreateView, CategoryDetailView, \
    CategoryDeleteView, CategoryUpdateView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('new/', CategoryCreateView.as_view(), name='category_create'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]

