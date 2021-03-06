""" views for the deal module """
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from snakelib.django.forms import field_queryset_exclude
from bid.forms import BidForm
from user.models import User
from calculator.models import VirtualDeal
from .models import Deal
from .forms import DealCreateForm


class DealListView(LoginRequiredMixin, ListView):  # pylint: disable=too-many-ancestors
    """ ListView for deal objects """
    template_name = 'deal/deal_list.html'
    context_object_name = 'deals'

    def get_queryset(self):
        return self.request.user.deals


class DealDetailView(LoginRequiredMixin, DetailView):
    """ DetailView of a single deal """
    model = Deal
    template_name = 'deal/deal_detail.html'

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        context['can_bid'] = self.object.can_bid(self.request.user)
        context['can_accept'] = self.object.can_accept(self.request.user)
        if context['can_bid']:
            context['push_form'] = BidForm(self.object.pushs)
            context['pull_form'] = BidForm(self.object.partner_pushs)
        context['chat'] = self.object.chat
        return context

    def get_object(self, queryset=None):
        deal = DetailView.get_object(self, queryset=queryset)
        deal.set_pov(self.request.user)
        return deal


class DealCreateView(LoginRequiredMixin, CreateView):
    """ CreateView for creating new deals """
    template_name = 'deal/deal_form.html'
    form_class = DealCreateForm

    def get_form(self, form_class=None):
        form = CreateView.get_form(self, form_class=form_class)
        form.fields['user2'].queryset = User.get_users().exclude(
            pk=self.request.user.pk
            )
        return form

    def form_valid(self, form):
        form.instance.user1 = self.request.user
        return CreateView.form_valid(self, form)

    def get_success_url(self):
        return reverse('deal_detail', args=(self.object.pk,))


class DealUserCreateView(LoginRequiredMixin, CreateView):
    """ CreateView for creating deals directly with a user """
    template_name = 'deal/deal_form.html'
    model = Deal
    fields = []
    user1, user2 = 2 * [None]

    def get_form(self, form_class=None):
        form = CreateView.get_form(self, form_class=form_class)
        self.user1 = self.request.user
        self.user2 = User.objects.get(
            pk=self.request.resolver_match.kwargs.get('partner_pk')
            )
        form.instance.user1 = self.user1
        form.instance.user2 = self.user2
        return form

    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['deal'] = VirtualDeal().by_user(self.user1, self.user2, level=0)
        return context

    def get_success_url(self):
        return reverse('deal_detail', args=(self.object.pk,))


class DealAcceptedView(LoginRequiredMixin, UpdateView):
    """ UpdateView for accepting a deal """
    model = Deal
    http_method_names = ['post']
    fields = []

    def post(self, request, *args, **kwargs):
        response = UpdateView.post(self, request, *args, **kwargs)
        self.object.set_accepted()
        return response

    def get_success_url(self):
        return reverse('deal_detail', args=(self.object.pk,))
