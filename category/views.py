from django.shortcuts import render
from .models import Category
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView


class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return ListView.get_queryset(self)


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
