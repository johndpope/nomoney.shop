from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from action.models import Action
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls.base import reverse_lazy


class ActionListView(ListView):
    model = Action


class ActionDetailView(DetailView):
    model = Action


class ActionCreateView(CreateView):
    model = Action
    fields = ['title', 'text']


class ActionUpdateView(UpdateView):
    model = Action
    fields = ['title', 'text']
    success_url = reverse_lazy('action-list')


class ActionDeleteView(DeleteView):
    model = Action
    success_url = reverse_lazy('action-list')
