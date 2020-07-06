from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormView
from django.views.generic.base import TemplateView
from django.urls.base import reverse_lazy, reverse
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from .models import UserConfig

User = get_user_model()  # pylint: disable=invalid-name
FIELDS = ['username', 'first_name', 'last_name', 'email', 'image', 'description']


class UserListView(LoginRequiredMixin, ListView):
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

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class UserSettingsView(LoginRequiredMixin, UpdateView):
    model = UserConfig
    #fields = FIELDS
    fields = '__all__'
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user.config

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        if self.object != self.request.user:
            context['chat'] = self.object.get_chat_with(self.request.user)
        return context


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
