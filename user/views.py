from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormView
from django.views.generic.base import TemplateView
from django.urls.base import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

User = get_user_model()  # pylint: disable=invalid-name
FIELDS = ['username', 'first_name', 'last_name', 'email']


class UserListView(ListView):
    model = User
    context_object_name = 'users'


class UserCreateView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = FIELDS
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('home')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        partner = self.model.objects.get(pk=kwargs.get('pk'))
        #=======================================================================
        # self.extra_context = {
        #     'deal': user.get_dealset_from_partner(partner).deal
        #     }
        #=======================================================================
        return DetailView.dispatch(self, request, *args, **kwargs)


class AgentView(LoginRequiredMixin, TemplateView):
    template_name = 'user/agent.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        user = self.request.user
        context['level1_deals'] = 'level1'
        context['level2_deals'] = user.virtual_dealsets
        context['level3_deals'] = 'level3'
        quality = [dealset.quality for dealset in context['level2_deals']]
        context['level2_quality_factor'] = 100 / max(quality) if quality else 0
        return context
