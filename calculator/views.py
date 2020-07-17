""" views for the calculator module """
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from chat.models import Chat
from .models import VirtualDeal


class CalculatorView(TemplateView):
    """ Main view of the calculator """
    template_name = 'calculator/calculator.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['lobby'] = Chat.get_lobby()
        return context


class AjaxDirectDealsView(LoginRequiredMixin, TemplateView):
    """ ajax view for direct deals """
    template_name = 'calculator/ajax/ajax_direct_deals.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['is_virtual'] = True
        context['deals_2d'] = VirtualDeal.by_users(
            self.request.user,
            self.request.user.other_users
            )
        return context


class AjaxTriangularDealsView(LoginRequiredMixin, TemplateView):
    """ ajax view for triangular deals """
    template_name = 'calculator/ajax/ajax_triangular_deals.html'


class AjaxSpeculativeDealsView(LoginRequiredMixin, TemplateView):
    """ ajax view for speculative deals """
    template_name = 'calculator/ajax/ajax_speculative_deals.html'
