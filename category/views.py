from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from .models import Category, CategoryStatus


class CategoryListView(LoginRequiredMixin, ListView):
    """ list categories in tree form """
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = sorted(
            Category.objects.exclude(
                status__in=(CategoryStatus.HIDDEN, CategoryStatus.DELETED,)
                ), key=lambda x: x.path
            )
        if self.request.user.is_staff:
            return queryset + list(Category.get_deleted()) + list(Category.get_hidden())
        return queryset


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

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            self.fields = self.fields + ['status']
        return LoginRequiredMixin.dispatch(self, request, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class CategoryAjaxView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'category/solo/category_detail.html'
