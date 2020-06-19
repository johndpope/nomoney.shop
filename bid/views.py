from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView
from .models import Bid
from .forms import BidForm, BidPushForm, BidPullForm
from django.views.generic.base import TemplateView

MODEL = Bid


class BidOverView(ListView):
    """ View all Bids from or to me """
    model = MODEL


class BidListView(ListView):
    """ List Bids of me from or to one partner """
    model = MODEL
    context_object_name = 'bids'


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
        if bid_form.is_valid():
            bid = bid_form.save(commit=True)
        import pdb; pdb.set_trace()  # <---------
        for form in push_forms + pull_forms:
            if form.is_valid():
                obj = form.save(bid=bid)
            
        #
        # jeweils für push und pull save bidpositions wenmn valid
        # save bid mit positions if valid
        return super().post(*args, **kwargs)


class BidDetailView(DetailView):
    """ Detail of one Bid """
    model = MODEL


class BidDeleteView(DeleteView):
    """ Delete BID by ID """
    model = MODEL
