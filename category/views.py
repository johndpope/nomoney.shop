from django.shortcuts import render
from .models import Category
from django.views.generic.list import ListView


class ListingListView(ListView):
    model = Category
    template_name = 'listing/listing_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return ListView.get_queryset(self)
