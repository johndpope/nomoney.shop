from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category


class CategoryListView(LoginRequiredMixin, ListView):
    """ list categories in tree form """
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'category/category_form.html'
    fields = ['parent', 'title', 'description']


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'category/category_detail.html'


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'category/category_form.html'


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category/category_delete.html'


class CategoryAjaxView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'category/solo/category_detail.html'
