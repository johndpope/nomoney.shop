from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormView
from django.urls.base import reverse_lazy
from django.contrib.auth import login, forms
from django.shortcuts import redirect
from .models import User
from django.views.generic.base import TemplateView

FIELDS = ['username', 'first_name', 'last_name', 'email']


class UserListView(ListView):
    model = User
    context_object_name = 'users'


class UserCreateView(FormView):
    form_class = forms.UserCreationForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class UserUpdateView(UpdateView):
    model = User
    fields = FIELDS
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('home')


class UserDetailView(DetailView):
    model = User


class AgentView(TemplateView):
    template_name = 'user/agent.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        user = self.request.user
        _, level1, level2, level3 = user.get_dealsets()
        context['level1_deals'] = level1
        context['level2_deals'] = level2
        context['level3_deals'] = level3
        return context
