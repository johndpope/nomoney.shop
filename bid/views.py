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


class BidCreateView(TemplateView):
    """ Create new Bid """
    template_name = 'bid/bid_form.html'
    partner = None
    dealset = None

    def dispatch(self, request, partner_pk, *args, **kwargs):
        user_class = request.user.__class__
        self.partner = user_class.objects.get(pk=partner_pk)
        self.dealset = request.user.get_dealset_from_partner(self.partner)
        return TemplateView.dispatch(self, request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        push_forms = []
        for push in self.dealset.deal.pushs:
            push_forms.append(BidPushForm(push, self.request.POST or None))
        context['push_forms'] = push_forms

        pull_forms = []
        for pull in self.dealset.deal.pulls:
            pull_forms.append(BidPullForm(pull, self.request.POST or None))
        context['pull_forms'] = pull_forms

        context['form'] = BidForm(self.partner)
        return context

    #form_class = BidForm
    #partner = None


    #===========================================================================
    # def get_form(self, form_class=None):
    #     """Return an instance of the form to be used in this view."""
    #     if form_class is None:
    #         form_class = self.get_form_class()
    #     return form_class(self.partner, **self.get_form_kwargs())
    #===========================================================================


class BidDetailView(DetailView):
    """ Detail of one Bid """
    model = MODEL


class BidDeleteView(DeleteView):
    """ Delete BID by ID """
    model = MODEL
