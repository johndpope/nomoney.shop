from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from .models import Deal
from django.urls.base import reverse


class DealListView(ListView):
    model = Deal

    def get_queryset(self):
        return self.request.user.deals


class DealDetailView(DetailView):
    model = Deal


class DealCreateView(CreateView):
    model = Deal
    fields = '__all__'

    def get_success_url(self):
        return reverse('deal_detail', args=(self.object.pk,))


class DealUpdateView(UpdateView):
    pass
