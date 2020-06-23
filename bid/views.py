from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView
from django.shortcuts import redirect
from .models import Bid, BidTopic
from .forms import BidForm, BidPushForm, BidPullForm

MODEL = Bid


class BidOverView(ListView):
    """ View all Bids from or to me """
    model = MODEL
    context_object_name = 'bids'
    template_name = 'bid/bid_list.html'

    def get_queryset(self):
        return Bid.topics_by_user(self.request.user)


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
        #=======================================================================
        # import pdb; pdb.set_trace()  # <---------
        # filter_ = (self.request.user, self.partner)
        # return self.model.objects.filter(user__in=filter_, partner__in=filter_)
        #=======================================================================
        return BidTopic(users=[self.request.user, self.partner]).bids


class BidCreateView(FormView):
    """ Create new Bid """
    template_name = 'bid/bid_form.html'
    partner = None
    dealset = None

    def setup(self, request, *args, **kwargs):
        FormView.setup(self, request, *args, **kwargs)
        user_class = request.user.__class__
        partner_pk = kwargs.get('partner_pk')
        self.partner = user_class.objects.get(pk=partner_pk)
        self.dealset = request.user.get_dealset_from_partner(self.partner)

    def get_forms(self):
        push_forms, pull_forms = [], []
        for push in self.dealset.deal.pushs:
            push_forms.append(BidPushForm(push, self.request.POST or None))
        for pull in self.dealset.deal.pulls:
            pull_forms.append(BidPullForm(pull, self.request.POST or None))
        return push_forms, pull_forms, BidForm(self.partner)

    def get_form(self, form_class=None):
        return self.get_forms()[2]

    def get_context_data(self, **kwargs):
        forms = self.get_forms()
        kwargs['push_forms'], kwargs['pull_forms'], kwargs['form'] = forms
        context = FormView.get_context_data(self, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        push_forms, pull_forms, bid_form = self.get_forms()
        bid = bid_form.save(commit=False)
        bid.user = self.request.user
        bid.partner = self.partner
        bid.save()
        for push_form in push_forms:
            if push_form.is_valid() and push_form.cleaned_data['quantity']:
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
