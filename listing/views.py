""" views for the listing module """
from copy import copy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls.base import reverse_lazy, reverse
from django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from category.models import Category
from calculator.models import VirtualDeal
from .models import Push, Pull


FIELDS = ['title', 'image', 'category', 'quantity', 'unit', 'description', 'location']
"""
listing_list - list pushs and pulls
listing_create
listing_update
listing_detail
"""


class DispatchMixin(View):
    model = None

    def dispatch(self, request, *args, **kwargs):
        self.type = kwargs.get('type')
        self.model = {'push': Push, 'pull': Pull}.get(self.type)
        if not self.model:
            url_name = request.resolver_match
            self.model = {'push_detail': Push, 'pull_detail': Pull}.get(url_name)
        response = super().dispatch(request, *args, **kwargs)
        self.extra_context = {'type': self.type}
        return response

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class ListingListView(LoginRequiredMixin, TemplateView):
    """ List of all listings """
    template_name = 'listing/listing_list.html'


# pylint: disable=too-many-ancestors
class ListingTypeListView(DispatchMixin, LoginRequiredMixin, ListView):
    """ List of all listings of a type """
    model = None
    template_name = 'listing/listing_list.html'

    def get_queryset(self):
        return self.model.objects.all()


class ListingCreateUpdateBase(DispatchMixin, LoginRequiredMixin, CreateView):
    """ base class for create and update view """
    model, category, type = 3 * [None]
    template_name = 'listing/listing_form.html'
    fields = FIELDS
    category = None

    def setup(self, request, *args, **kwargs):
        CreateView.setup(self, request, *args, **kwargs)
        if 'category_pk' in self.kwargs:
            self.category = Category.objects.get(
                pk=self.kwargs.get('category_pk')
                )
            self.fields = copy(ListingCreateView.fields)
            self.fields.remove('category')

    def get_form(self, form_class=None):
        form = CreateView.get_form(self, form_class=form_class)
        form.fields['location'].queryset = self.request.user.locations
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.category:
            form.instance.category = self.category
        return super().form_valid(form)


class ListingCreateView(ListingCreateUpdateBase, CreateView):
    """ CreateView for creating new listings """


class ListingUpdateView(ListingCreateUpdateBase, UpdateView):
    """ UpdateView for updating existing listings """


class ListingDetailView(DispatchMixin, LoginRequiredMixin, DetailView):
    """ DetailView to view a single listing """
    template_name = 'listing/listing_detail.html'
    context_object_name = 'listing'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = DetailView.get_context_data(self, **kwargs)
        listing = kwargs['object']
        partner = listing.user
        context['deal'] = VirtualDeal.by_user(user, partner)
        context['chat'] = listing.get_chat_with_partner(partner)
        return context


class ListingDeleteView(DispatchMixin, LoginRequiredMixin, DeleteView):
    """ DeleteView to delete a listing """
    template_name = 'listing/listing_delete.html'


