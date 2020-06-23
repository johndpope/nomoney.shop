from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView


class ChatListView(ListView):
    pass


class ChatDetailView(DetailView):
    pass


class ChatCreateView(CreateView):
    pass


class ChatNewMessageView(CreateView):
    pass

