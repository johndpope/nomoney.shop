""" views for the user module """
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormView
from django.urls.base import reverse_lazy, reverse
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from chat.models import Chat
from action.models import create_action
from calculator.models import VirtualDeal
from .forms import CustomUserCreationForm, CustomUserLoginForm
from .models import User, UserConfig

FIELDS = ['username', 'first_name', 'last_name', 'email', 'image', 'description']


class UserLoginView(LoginView):
    form_class = CustomUserLoginForm
    template_name = 'user/user_login.html'


# pylint: disable=too-many-ancestors
class UserListView(LoginRequiredMixin, ListView):
    """ ListView to list all users """
    model = User
    context_object_name = 'users'

    def get_queryset(self):
        return User.get_users()

    def get_context_data(self, *args, **kwargs):
        context = ListView.get_context_data(self, *args, **kwargs)
        context['chat'] = Chat.get_lobby()
        return context


class UserCreateView(FormView):
    """ FormView to Create new user """
    form_class = CustomUserCreationForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """ UpdateView to update user informations """
    model = User
    fields = FIELDS
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class UserSettingsView(LoginRequiredMixin, UpdateView):
    """ UpdateView for updating UserConfig """
    model = UserConfig
    fields = '__all__'
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user.config

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class UserDetailView(LoginRequiredMixin, DetailView):
    """ DetailView to view a single user """
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        create_action(self.request.user, 'USER_CREATED')
        context = DetailView.get_context_data(self, **kwargs)
        if self.object != self.request.user:
            context['chat'] = self.object.get_chat_with(self.request.user)
            context['deal'] = VirtualDeal.combinated(
                self.object, me_=self.request.user
            )[0]
        return context
