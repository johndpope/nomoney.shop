from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from listing.models import Listing


class CalculatorView(TemplateView):
    template_name = 'user/calculator.html'


class PushView(ListView):
    model = Listing


class PullView(ListView):
    model = Listing
