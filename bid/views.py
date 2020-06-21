from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView
from django.views.generic.base import TemplateView
from django.urls.base import reverse_lazy
from django.shortcuts import redirect
from .models import Bid
from .forms import BidForm, BidPushForm, BidPullForm

MODEL = Bid


class BidOverView(ListView):
    """ View all Bids from or to me """
    model = MODEL
    context_object_name = 'bids'


class BidListView(ListView):
    """ List Bids of me from or to one partner """
    model = MODEL
    context_object_name = 'bids'
    partner = None

    def dispatch(self, request, *args, **kwargs):
        partner_pk = kwargs.get('partner_pk')
        user_class = request.user.__class__
        self.partner = user_class.objects.get(pk=partner_pk)
        return ListView.dispatch(self, request, *args, **kwargs)

    def get_queryset(self):
        filter_ = (self.request.user, self.partner)
        return self.model.objects.filter(user__in=filter_, partner__in=filter_)


class BidCreateView(FormView):
    """ Create new Bid """
    template_name = 'bid/bid_form.html'
    partner = None
    dealset = None

    def dispatch(self, request, partner_pk, *args, **kwargs):
        user_class = request.user.__class__
        self.partner = user_class.objects.get(pk=partner_pk)
        self.dealset = request.user.get_dealset_from_partner(self.partner)
        return TemplateView.dispatch(self, request, *args, **kwargs)

    def get_forms(self):
        push_forms, pull_forms = [], []
        for push in self.dealset.deal.pushs:
            push_forms.append(BidPushForm(push, self.request.POST or None))
        for pull in self.dealset.deal.pulls:
            pull_forms.append(BidPullForm(pull, self.request.POST or None))
        return push_forms, pull_forms, BidForm(self.partner)

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        forms = self.get_forms()
        context['push_forms'], context['pull_forms'], context['form'] = forms
        return context

    def post(self, *args, **kwargs):
        push_forms, pull_forms, bid_form = self.get_forms()
        bid = bid_form.save(commit=False)
        bid.user = self.request.user
        bid.partner = self.partner
        bid.save()
        for push_form in push_forms:
            if push_form.is_valid():
                push_form.save(bid)
        for pull_form in pull_forms:
            if pull_form.is_valid():
                pull_form.save(bid)
        bid.save()
        return redirect(reverse_lazy('home'))


class BidDetailView(DetailView):
    """ Detail of one Bid """
    model = MODEL


class BidDeleteView(DeleteView):
    """ Delete BID by ID """
    model = MODEL
