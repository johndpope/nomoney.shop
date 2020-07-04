from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import VirtualDeal


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_home.html'

    def get_context_data(self, **kwargs):
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
        else:
            self.template_name = 'dashboard/dashboard_anonymous.html'
        return context


class Ajax2dView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/ajax_2d.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['is_virtual'] = True
        context['deals_2d'] = VirtualDeal.by_users(
            self.request.user,
            self.request.user.other_users
            )
        return context


class Ajax3dView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/ajax_3d.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        return context
