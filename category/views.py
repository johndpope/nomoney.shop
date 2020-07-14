from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from .models import Category


class CategoryListView(LoginRequiredMixin, ListView):
    """ list categories in tree form """
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(test=self.request.user.test)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'category/category_form.html'
    fields = ['parent', 'title', 'description']

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'category/category_detail.html'


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'category/category_form.html'
    fields = ['parent', 'title', 'description']

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class CategoryAjaxView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'category/solo/category_detail.html'
