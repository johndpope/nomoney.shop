from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView
from django.shortcuts import redirect
from .models import Bid, BidPush, BidPull
from .forms import BidForm, BidPushForm, BidPullForm
from deal.models import Deal

MODEL = Bid


class BidListView(ListView):
    """ List Bids of me from or to one partner """
    model = MODEL

    def get_queryset(self):
        return self.model.by_user(self.request.user)


class BidCreateView(FormView):
    """ Create new Bid """
    template_name = 'bid/bid_form.html'
    deal = None
    #form_class = BidForm
 
    def setup(self, request, *args, **kwargs):
        FormView.setup(self, request, *args, **kwargs)
        deal_pk = kwargs.get('deal_pk')
        self.deal = Deal.objects.get(pk=deal_pk)
        self.deal.set_pov(self.request.user)
 
    def get(self, request, *args, **kwargs):
        push_form = BidForm(self.deal.pushs)
        pull_form = BidForm(self.deal.pulls)
        return self.render_to_response({
            'push_form': push_form,
            'pull_form': pull_form,
            })
 
    def post(self, request, *args, **kwargs):
        push_form = BidForm(self.deal.pushs, request.POST)
        pull_form = BidForm(self.deal.pulls, request.POST)
        if push_form.is_valid() and pull_form.is_valid():
            bid = Bid.objects.create(deal=self.deal, creator=request.user)
            for key, value in push_form.cleaned_data.items():
                print(request.POST)
                if value:
                    BidPush.objects.create(
                        listing=push_form.fields[key].listing,
                        unit=push_form.fields[key].unit,
                        quantity=value,
                        bid=bid
                        )
            for key, value in pull_form.cleaned_data.items():
                print(request.POST)
                if value:
                    BidPull.objects.create(
                        listing=pull_form.fields[key].listing,
                        unit=pull_form.fields[key].unit,
                        quantity=value,
                        bid=bid
                        )
            return redirect('deal_detail', pk=self.deal.pk)
        else:
            return self.render_to_response({
                'push_form': push_form,
                'pull_form': pull_form,
                })


class BidDetailView(DetailView):
    """ Detail of one Bid """
    model = MODEL


class BidDeleteView(DeleteView):
    """ Delete BID by ID """
    model = MODEL
