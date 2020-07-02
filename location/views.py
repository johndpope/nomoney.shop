from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls.base import reverse
from .models import Location


class LocationListView(ListView):
    model = Location

    def get_queryset(self):
        return self.request.user.locations


class LocationDetailView(DetailView):
    model = Location


class LocationCreateView(CreateView):
    model = Location
    fields = ['title', 'lon', 'lat', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return UpdateView.form_valid(self, form)

    def get_success_url(self):
        return reverse('location_detail', args=(self.object.pk, ))


class LocationUpdateView(UpdateView):
    model = Location
    fields = ['title', 'lon', 'lat', 'description']

    def get_success_url(self):
        return reverse('location_detail', args=(self.object.pk, ))


class LocationDeleteView(DeleteView):
    model = Location
    template_name = 'guild/guild_delete.html'

    def get_success_url(self):
        return reverse('guild_list')
