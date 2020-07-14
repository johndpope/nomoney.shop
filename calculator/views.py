from django.views.generic.base import TemplateView
from chat.models import Chat


class CalculatorView(TemplateView):
    template_name = 'calculator/calculator.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['lobby'] = Chat.get_lobby()
        return context
