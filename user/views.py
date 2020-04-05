from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from listing.models import Push
from django.views.generic.list import ListView


class CalculatorView(TemplateView):
    template_name = 'user/calculator.html'


class PushView(ListView):
    model = Push

    def get_queryset(self):
        return ListView.get_queryset(self)


class PullView(ListView):
    model = Push
