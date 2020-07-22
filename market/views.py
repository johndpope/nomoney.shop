""" views for the market module """
from django.views.generic.edit import DeleteView, UpdateView, CreateView,\
    FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from calculator.models import VirtualDeal
from user.models import User
from .models import Market


# pylint: disable=too-many-ancestors
class MarketListView(LoginRequiredMixin, ListView):
    """ ListView of markets """
    model = Market
    context_object_name = 'markets'

    def get_queryset(self):
        return self.request.user.market_set.all()


class MarketDetailView(LoginRequiredMixin, DetailView):
    """ DetailView of a single market """
    model = Market

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        context['deals_2d'] = VirtualDeal.combinated(
            *self.object.users.all(),
            me_=self.request.user
            )
        context['chat'] = self.object.chat
        return context


class MarketCreateUpdateBase(LoginRequiredMixin, FormView):
    """ Base for CreateView and UpdateView """
    model = Market
    fields = ['title', 'users', 'location']

    def get_form(self, form_class=None):
        form = CreateView.get_form(self, form_class=form_class)
        form.fields['users'].widget.attrs['class'] = 'chosen-select'
        form.fields['users'].widget.attrs['data-placeholder'] = \
            'Benutzer auswählen ...'
        form.fields['users'].queryset = User.get_users().exclude(
            pk=self.request.user.pk)
        form.fields['location'].queryset = self.request.user.locations
        return form

    def form_valid(self, form):
        response = CreateView.form_valid(self, form)
        form.instance.users.add(self.request.user)
        form.instance.save()
        return response

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class MarketCreateView(MarketCreateUpdateBase, CreateView):
    """ CreateView for creating new market """


class MarketUpdateView(MarketCreateUpdateBase, UpdateView):
    """ UpdateView to update existing market """


class MarketDeleteView(LoginRequiredMixin, DeleteView):
    """ DeleteView to delete a market """
    model = Market
    template_name = 'market/market_delete.html'

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))
