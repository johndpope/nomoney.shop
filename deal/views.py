from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Deal
from .forms import DealCreateForm, DealAcceptForm
from bid.forms import BidForm
from user.models import User
from dashboard.models import VirtualDeal
# TODO: check if access is allowed (self.request.user in dealset user


class DealListView(LoginRequiredMixin, ListView):
    model = Deal
    template_name = 'deal/deal_list.html'

    def get_queryset(self):
        return self.request.user.deals


class DealDetailView(LoginRequiredMixin, DetailView):
    model = Deal
    template_name = 'deal/deal_detail.html'

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        context['can_bid'] = self.object.can_bid(self.request.user)
        context['can_accept'] = self.object.can_accept(self.request.user)
        if context['can_bid']:
            context['push_form'] = BidForm(self.object.pushs)
            context['pull_form'] = BidForm(self.object.pulls)
        return context


class DealCreateView(LoginRequiredMixin, CreateView):
    template_name = 'deal/deal_form.html'
    form_class = DealCreateForm

    def form_valid(self, form):
        form.instance.user1 = self.request.user
        return CreateView.form_valid(self, form)

    def get_success_url(self):
        return reverse('deal_detail', args=(self.object.pk,))


class DealUserCreateView(LoginRequiredMixin, UpdateView):
    model = Deal
    fields = []

    def get_object(self, queryset=None):
        partner_pk = self.request.resolver_match.kwargs.get('partner_pk')
        partner = User.objects.get(pk=partner_pk)
        self.extra_context = {'deal': VirtualDeal(self.request.user, partner)}
        return Deal.get_or_create((self.request.user, partner))

    def get_success_url(self):
        return reverse('deal_detail', args=(self.object.pk,))


class DealAcceptedView(LoginRequiredMixin, UpdateView):
    #form_class = DealAcceptForm
    model = Deal
    http_method_names = ['post']
    fields = ['accepted']

    def post(self, request, *args, **kwargs):
        response = UpdateView.post(self, request, *args, **kwargs)
        if self.request.user in self.object.bid_allowed_for():
            self.object.accepted = True
            self.object.save()
        return response

    def get_success_url(self):
        return reverse('deal_detail', args=(self.object.pk,))
