from django.views.generic.base import TemplateView
from .models import VirtualDeal
from django.views.decorators.cache import cache_page


class DashboardHomeView(TemplateView):
    template_name = 'dashboard/dashboard_home.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        return context


class Ajax2dView(TemplateView):
    template_name = 'dashboard/ajax_2d.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['is_virtual'] = True
        context['deals_2d'] = VirtualDeal.by_users(
            self.request.user,
            self.request.user.other_users
            )
        return context


class Ajax3dView(TemplateView):
    template_name = 'dashboard/ajax_3d.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        return context
