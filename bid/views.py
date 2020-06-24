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
                if value:
                    BidPush.objects.create(
                        listing=push_form.fields[key].listing,
                        unit=push_form.fields[key].unit,
                        quantity=value,
                        bid=bid
                        )
            for key, value in pull_form.cleaned_data.items():
                if value:
                    BidPull.objects.create(
                        listing=pull_form.fields[key].listing,
                        unit=pull_form.fields[key].unit,
                        quantity=value,
                        bid=bid
                        )
            return redirect('deal_detail', pk=self.deal.dealset.pk)
        else:
            return self.render_to_response({
                'push_form': push_form,
                'pull_form': pull_form,
                })

#===============================================================================
#     def setup(self, request, *args, **kwargs):
#         FormView.setup(self, request, *args, **kwargs)
#         deal_pk = kwargs.get('deal_pk')
#         self.deal = Deal.objects.get(pk=deal_pk)
# 
#     def get_forms(self):
#         push_forms, pull_forms = [], []
#         for push in self.deal.pushs:
#             push_form = BidPushForm(push, self.request.POST or None)
#             push_forms.append(push_form)
#         for pull in self.deal.pulls:
#             pull_form = BidPullForm(pull, self.request.POST or None)
#             pull_forms.append(pull_form)
#         return push_forms, pull_forms, BidForm(self.deal, self.request.user)
# 
#     def get_form(self, form_class=None):
#         return self.get_forms()[2]
# 
#     def get_context_data(self, **kwargs):
#         forms = self.get_forms()
#         kwargs['push_forms'], kwargs['pull_forms'], kwargs['form'] = forms
#         context = FormView.get_context_data(self, **kwargs)
#         return context
# 
#     def post(self, request, *args, **kwargs):
#         push_forms, pull_forms, _ = self.get_forms()
#         bid = Bid.objects.create(deal=self.deal, creator=request.user)
#         for push_form in push_forms:
#             if push_form.is_valid() and push_form.cleaned_data['quantity']:
#                 push_form.save(bid)
#                 bid.pushs.add()
#  
#         for pull_form in pull_forms:
#             if pull_form.is_valid() and pull_form.cleaned_data['quantity']:
#                 bid.pulls.add(pull_form.save(bid))
#         bid.save()
#         return redirect('deal_detail', partner_pk=self.deal.dealset.pk)
#===============================================================================


class BidDetailView(DetailView):
    """ Detail of one Bid """
    model = MODEL


class BidDeleteView(DeleteView):
    """ Delete BID by ID """
    model = MODEL
