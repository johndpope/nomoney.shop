from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Bid
from .forms import BidForm
from listing.models import Unit


class BidView():
    pass


class BidCreateView(TemplateView):
    """
    TODO:
    Post
    Get - Letztes Gebot ansehen
    """
    #form_class = BidForm
    template_name = 'bid/bid_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user

        user_class = self.request.user.__class__
        context['partner'] = user_class.objects.get(pk=kwargs.get('partner_pk'))

        context['pushs'] = [push for push in context['user'].pushs
                            if push in context['partner'].pulls]
        context['pulls'] = context['partner'].pushs
        context['units'] = Unit.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()  # <---------
