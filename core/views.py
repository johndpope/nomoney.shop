""" views of the core module """
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from chat.models import Chat
from action.models import create_action, TASKS
from action.exp import Level


class AboutView(TemplateView):
    """ /about/ """
    template_name = 'sites/about.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['tasks'] = sorted(TASKS)
        context['levels'] = Level.levels()
        return context


class DonateView(TemplateView):
    """ /donate/ """
    template_name = 'sites/donate.html'


class TermsView(TemplateView):
    """ /terms-and-conditions/ """
    template_name = 'sites/terms.html'


class ImpressumView(TemplateView):
    """ /impressum/ """
    template_name = 'sites/impressum.html'


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """ / """
    template_name = 'dashboard/dashboard_home.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            create_action(self.request.user, 'DAILY_VISIT')
        context = TemplateView.get_context_data(self, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            deals = []
            for deal in user.deals:
                deals.append(deal.set_pov(self.request.user))
            context['deals'] = deals
            context['user_feedback_open'] = user.userfeedback_set.filter(
                status=0
                )
            context['push_feedback_open'] = user.pushfeedback_set.filter(
                status=0
                )
            context['lobby'] = Chat.get_lobby()
            # context['chat'] = Chat.get_lobby()
        else:
            self.template_name = 'dashboard/dashboard_anonymous.html'
        return context
