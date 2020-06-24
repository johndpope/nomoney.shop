from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView
from django.shortcuts import redirect
from .models import Bid
from .forms import BidForm, BidPushForm, BidPullForm
from deal.models import DealSet

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

    def setup(self, request, *args, **kwargs):
        FormView.setup(self, request, *args, **kwargs)
        deal_pk = kwargs.get('deal_pk')
        self.deal = DealSet.objects.get(pk=deal_pk)

    def get_forms(self):
        push_forms, pull_forms = [], []
        for push in self.deal.pushs:
            push_forms.append(BidPushForm(push, self.request.POST or None))
        for pull in self.deal.pulls:
            pull_forms.append(BidPullForm(pull, self.request.POST or None))
        return push_forms, pull_forms, BidForm(self.deal)

    def get_form(self, form_class=None):
        return self.get_forms()[2]

    def get_context_data(self, **kwargs):
        forms = self.get_forms()
        kwargs['push_forms'], kwargs['pull_forms'], kwargs['form'] = forms
        context = FormView.get_context_data(self, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        deal = Deal.open((self.request.user, self.partner))
        push_forms, pull_forms, bid_form = self.get_forms()
        bid = bid_form.save(commit=False)
        bid.deal = deal
        bid.creator = self.request.user
        bid.save()
        for push_form in push_forms:
            if push_form.is_valid() and push_form.cleaned_data['quantity']:
                import pdb; pdb.set_trace()  # <---------
                push_form.save(bid)
        for pull_form in pull_forms:
            if pull_form.is_valid() and pull_form.cleaned_data['quantity']:
                pull_form.save(bid)
        bid.save()
        return redirect('bid_list', partner_pk=self.partner.pk)


class BidDetailView(DetailView):
    """ Detail of one Bid """
    model = MODEL


class BidDeleteView(DeleteView):
    """ Delete BID by ID """
    model = MODEL
