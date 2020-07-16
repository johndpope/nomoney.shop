""" views of the search module """
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SearchForm
from .models import SearchEngine


class SearchView(LoginRequiredMixin, FormView):
    """ main view of the search form (not used) """
    form_class = SearchForm
    template_name = 'search/basic.html'

    def get(self, request, *args, **kwargs):
        if 's' in request.GET:  # Returns result
            raise NotImplementedError('not yet implemented')
        return FormView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'text' in request.POST:
            text = request.POST.get('text')
        return redirect(reverse('search_basic') + '?s=' + text)


class AjaxPollView(LoginRequiredMixin, TemplateView):
    """ Ajax view for the realtime search """
    template_name = 'search/solo/search_live.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        results = SearchEngine(kwargs.get('search_string')).get_results()
        # results = SearchEngine(kwargs.get('search_string')).get_results()
        context['results'] = results or []
        return context
