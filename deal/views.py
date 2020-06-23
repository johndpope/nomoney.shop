from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView


class DealListView(ListView):
    pass


class DealDetailView(DetailView):
    pass


class DealCreateView(CreateView):
    pass


class DealUpdateView(UpdateView):
    pass
