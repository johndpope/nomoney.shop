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
from django.views.generic.base import TemplateView
# TODO: check if access is allowed (self.request.user in dealset user


class DealListView(LoginRequiredMixin, TemplateView):
    template_name = 'deal/deal_list.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        deals = []
        for deal in self.request.user.deals:
            deals.append(deal.set_pov(self.request.user))
        context['deals'] = deals
        return context


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

    def get_object(self, queryset=None):
        deal = DetailView.get_object(self, queryset=queryset)
        deal.set_pov(self.request.user)
        return deal


class DealCreateView(LoginRequiredMixin, CreateView):
    template_name = 'deal/deal_form.html'
    form_class = DealCreateForm

    def form_valid(self, form):
        form.instance.user1 = self.request.user
        return CreateView.form_valid(self, form)

    def get_success_url(self):
        return reverse('deal_detail', args=(self.object.pk,))


class DealUserCreateView(LoginRequiredMixin, CreateView):
    template_name = 'deal/deal_form.html'
    model = Deal
    fields = []

    def get_form(self, form_class=None):
        form = CreateView.get_form(self, form_class=form_class)
        form.instance.user1 = self.request.user
        form.instance.user2 = User.objects.get(
            pk=self.request.resolver_match.kwargs.get('partner_pk')
            )
        return form

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
