""" views for the bid module """
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from deal.models import Deal
from .models import Bid, BidPosition
from .forms import BidForm

MODEL = Bid


# pylint: disable=too-many-ancestors
class BidListView(LoginRequiredMixin, ListView):
    """ List Bids of me from or to one partner """
    model = MODEL

    def get_queryset(self):
        return self.model.by_user(self.request.user)


class BidCreateView(LoginRequiredMixin, FormView):
    """ Create new Bid """
    template_name = 'bid/bid_form.html'
    deal, bid = 2 * [None]

    def setup(self, request, *args, **kwargs):
        FormView.setup(self, request, *args, **kwargs)
        deal_pk = kwargs.get('deal_pk')
        self.deal = Deal.objects.get(pk=deal_pk)
        self.deal.set_pov(self.request.user)

    def get(self, request, *args, **kwargs):
        push_form = BidForm(self.deal.pushs)
        pull_form = BidForm(self.deal.partner_pushs)
        return self.render_to_response({
            'push_form': push_form,
            'pull_form': pull_form,
            })

    def post(self, request, *args, **kwargs):
        push_form = BidForm(self.deal.pushs, request.POST)
        pull_form = BidForm(self.deal.partner_pushs, request.POST)
        if push_form.is_valid() and pull_form.is_valid():
            self.bid = Bid.objects.create(deal=self.deal, creator=request.user)
            self.iter_form(push_form)
            self.iter_form(pull_form)
            return redirect('deal_detail', pk=self.deal.pk)
        return self.render_to_response({
            'push_form': push_form,
            'pull_form': pull_form,
            })

    def iter_form(self, form):
        """ iterate over form """
        for key, value in form.cleaned_data.items():
            if value:
                self.create_bidposition(form, key, value)

    def create_bidposition(self, form, key, value):
        """ create bid position """
        BidPosition.objects.create(
            push=form.fields[key].listing,
            unit=form.fields[key].unit,
            quantity=value,
            bid=self.bid
            )


class BidDetailView(LoginRequiredMixin, DetailView):
    """ Detail of one Bid """
    model = MODEL


class BidDeleteView(LoginRequiredMixin, DeleteView):
    """ Delete BID by ID """
    model = MODEL
