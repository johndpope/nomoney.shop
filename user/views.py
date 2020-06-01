from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from listing.models import Listing
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.urls.base import reverse_lazy
from django.contrib.auth import login, authenticate
from .models import User
from .forms import UserCreationForm
from django.shortcuts import redirect


class CalculatorView(TemplateView):
    template_name = 'user/calculator.html'


class PushView(ListView):
    model = Listing


class PullView(ListView):
    model = Listing


class UserListView(ListView):
    model = User
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'


class UserUpdateView(UpdateView):
    model = User
    fields = ['email', 'username']
    success_url = reverse_lazy('home')


class UserCreateView(FormView):
    form_class = UserCreationForm
    template_name = 'user/user_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class UserListingsView(ListView):
    model = Listing
    template_name = 'user/user_listings.html'
    context_object_name = 'listings'

    def get(self, request, *args, **kwargs):
        return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs.get('pk'))
        return Listing.objects.filter(user=user)
