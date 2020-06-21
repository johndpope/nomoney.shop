from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Category


class CategoryListView(ListView):
    """ list categories in tree form """
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'category/category_form.html'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category/category_detail.html'


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'category/category_form.html'


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/category_delete.html'
