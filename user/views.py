from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from listing.models import Listing
from .models import User
from django.views.generic.edit import UpdateView
from django.urls.base import reverse_lazy


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
