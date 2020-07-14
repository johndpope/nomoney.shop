from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from chat.models import Chat
from .models import VirtualDeal


class CalculatorView(TemplateView):
    template_name = 'calculator/calculator.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['lobby'] = Chat.get_lobby()
        return context


class AjaxDirectDealsView(LoginRequiredMixin, TemplateView):
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
    template_name = 'calculator/ajax/ajax_triangular_deals.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        return context


class AjaxSpeculativeDealsView(LoginRequiredMixin, TemplateView):
    template_name = 'calculator/ajax/ajax_speculative_deals.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        return context
