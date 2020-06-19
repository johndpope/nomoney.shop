from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import SearchForm
from django.views.generic.base import TemplateView
from django.urls.base import reverse
from .models import Search


class SearchView(FormView):
    form_class = SearchForm
    template_name = 'search/basic.html'

    def get(self, request, *args, **kwargs):
        if 's' in request.GET:  # Returns result
            users, categories, listings = [], [], []
            search = Search()
        return FormView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'text' in request.POST:
            text = request.POST.get('text')
            return redirect(reverse('search_basic') + '?s=' + text)
