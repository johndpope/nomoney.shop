from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Location


class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    context_object_name = 'locations'

    def get_queryset(self):
        return self.request.user.locations


class LocationDetailView(LoginRequiredMixin, DetailView):
    model = Location
    context_object_name = 'location'


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    fields = ['title', 'lon', 'lat', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return UpdateView.form_valid(self, form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    fields = ['title', 'lon', 'lat', 'description']

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location
    template_name = 'market/market_delete.html'

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))
