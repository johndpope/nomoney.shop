from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import SearchForm
from django.views.generic.base import TemplateView
from django.urls.base import reverse
from .models import SearchEngine


class SearchView(FormView):
    form_class = SearchForm
    template_name = 'search/basic.html'

    def get(self, request, *args, **kwargs):
        if 's' in request.GET:  # Returns result
            users, categories, listings = [], [], []
            search = None#SearchEngine()
        return FormView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'text' in request.POST:
            text = request.POST.get('text')
            return redirect(reverse('search_basic') + '?s=' + text)

class AjaxPollView(TemplateView):
    template_name = 'search/solo/search_live.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        results = SearchEngine(kwargs.get('search_string')).get_results()
        #results = SearchEngine(kwargs.get('search_string')).get_results()
        context['results'] = results or []
        return context