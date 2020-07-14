from copy import copy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls.base import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from category.models import Category
from core.models import VirtualDeal
from .models import Push, Pull
from django.contrib.auth.mixins import LoginRequiredMixin


FIELDS = ['title', 'image', 'category', 'quantity', 'unit', 'description', 'location']
"""
listing_list - list pushs and pulls
listing_create
listing_update
listing_detail
"""


class ListingListView(LoginRequiredMixin, TemplateView):
    template_name = 'listing/listing_list.html'


class ListingTypeListView(LoginRequiredMixin, ListView):
    model = None
    template_name = 'listing/listing_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.model = {'push': Push, 'pull': Pull}.get(kwargs.get('type'))
        return DetailView.dispatch(self, request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()


class ListingCreateView(LoginRequiredMixin, CreateView):
    model, category, type = 3 * [None]
    fields = FIELDS
    template_name = 'listing/listing_form.html'
    success_url = reverse_lazy('listing_list')
    category = None

    def setup(self, request, *args, **kwargs):
        CreateView.setup(self, request, *args, **kwargs)
        self.type = kwargs.get('type')
        self.model = {'push': Push, 'pull': Pull}.get(self.type)
        if 'category_pk' in self.kwargs:
            self.category = Category.objects.get(
                pk=self.kwargs.get('category_pk')
                )
            self.fields = copy(ListingCreateView.fields)
            self.fields.remove('category')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.category:
            form.instance.category = self.category
        return CreateView.form_valid(self, form)

    def get_form(self, form_class=None):
        form = CreateView.get_form(self, form_class=form_class)
        if 'category' in form.fields:
            form.fields['category'].queryset = form.fields['category'].queryset.filter(
                test=self.request.user.test)
        form.fields['location'].queryset = form.fields['location'].queryset.filter(
            test=self.request.user.test)
        return form

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class ListingUpdateView(LoginRequiredMixin, UpdateView):
    model, type = 2 * [None]
    template_name = 'listing/listing_form.html'
    fields = FIELDS
    success_url = reverse_lazy('listing_list')

    def dispatch(self, request, *args, **kwargs):
        self.type = kwargs.get('type')
        self.model = {'push': Push, 'pull': Pull}.get(self.type)
        self.extra_context = {'type': self.type}
        return DetailView.dispatch(self, request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = UpdateView.get_form(self, form_class=form_class)
        form.fields['category'].queryset = form.fields['category'].queryset.filter(
            test=self.request.user.test)
        form.fields['location'].queryset = form.fields['location'].queryset.filter(
            test=self.request.user.test)
        return form

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class ListingDetailView(LoginRequiredMixin, DetailView):  # OK
    model = None
    template_name = 'listing/listing_detail.html'
    context_object_name = 'listing'

    def dispatch(self, request, *args, **kwargs):
        self.model = {'push': Push, 'pull': Pull}.get(kwargs.get('type'))
        listing = self.model.objects.get(pk=kwargs.get('pk'))
        user = request.user
        partner = listing.user
        self.extra_context = {
            'deal': VirtualDeal.by_user(user, partner),
            'chat': listing.get_chat_with_partner(partner),
            }
        return DetailView.dispatch(self, request, *args, **kwargs)


class ListingDeleteView(LoginRequiredMixin, DeleteView):
    model = None
    template_name = 'listing/listing_delete.html'
    success_url = reverse_lazy('listing_list')

    def dispatch(self, request, *args, **kwargs):
        self.model = {'push': Push, 'pull': Pull}.get(kwargs.get('type'))
        return DeleteView.dispatch(self, request, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))
