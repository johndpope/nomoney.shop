from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from .models import Bid

MODEL = Bid


class BidOverView(ListView):
    """ View all Bids from or to me """
    model = MODEL


class BidListView(ListView):
    """ List Bids of me from or to one partner """
    model = MODEL


class BidCreateView(CreateView):
    """ Create new Bid """
    model = MODEL


class BidDetailView(DetailView):
    """ Detail of one Bid """
    model = MODEL


class BidDeleteView(DeleteView):
    """ Delete BID by ID """
    model = MODEL
