from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Listing
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls.base import reverse_lazy
from listing.models import Category


class ListingListView(ListView):
    model = Category
    template_name = 'listing/listing_list.html'
    context_object_name = 'categories'


class ListingDetailView(DetailView):
    model = Listing



class ListingCreateView(CreateView):
    model = Listing
    fields = ['title', 'text']


class ListingUpdateView(UpdateView):
    model = Listing
    fields = ['title', 'text']
    success_url = reverse_lazy('Listing-list')


class ListingDeleteView(DeleteView):
    model = Listing
    success_url = reverse_lazy('Listing-list')
