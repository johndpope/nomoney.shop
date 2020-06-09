from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Bid


class BidView():
    pass


class BidCreateView(CreateView):
    model = Bid
    fields = ['push_listing', 'push_quantity', 'push_unit', 'pull_listing', 
              'pull_quantity', 'pull_unit',]

    def get(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()  # <---------
        return CreateView.get(self, request, *args, **kwargs)