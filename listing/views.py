from copy import copy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls.base import reverse_lazy
from .models import Push, Pull
from category.models import Category
from django.views.generic.base import TemplateView

FIELDS = ['title', 'image', 'category', 'quantity', 'unit', 'description']
"""
listing_list - list pushs and pulls
listing_create
listing_update
listing_detail
"""


class ListingListView(TemplateView):
    template_name = 'listing/listing_list.html'


class ListingTypeListView(ListView):
    model = None
    template_name = 'listing/listing_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.model = {'push': Push, 'pull': Pull}.get(kwargs.get('type'))
        return DetailView.dispatch(self, request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()


class ListingCreateView(CreateView):
    model = None
    fields = FIELDS
    template_name = 'listing/listing_form.html'
    success_url = reverse_lazy('listing_list')
    category = None

    def setup(self, request, *args, **kwargs):
        CreateView.setup(self, request, *args, **kwargs)
        self.model = {'push': Push, 'pull': Pull}.get(self.kwargs.get('type'))
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


class ListingUpdateView(UpdateView):
    model = None
    template_name = 'listing/listing_form.html'
    fields = FIELDS
    success_url = reverse_lazy('listing_list')

    def dispatch(self, request, *args, **kwargs):
        self.model = {'push': Push, 'pull': Pull}.get(kwargs.get('type'))
        self.extra_context = {'type': kwargs.get('type')}
        return DetailView.dispatch(self, request, *args, **kwargs)


class ListingDetailView(DetailView):  # OK
    model = None
    template_name = 'listing/listing_detail.html'
    context_object_name = 'listing'

    def dispatch(self, request, *args, **kwargs):
        self.model = {'push': Push, 'pull': Pull}.get(kwargs.get('type'))
        listing = self.model.objects.get(pk=kwargs.get('pk'))
        user = request.user
        partner = listing.user
        self.extra_context = {
            'deal': user.get_dealset_from_partner(partner).deal
            }
        return DetailView.dispatch(self, request, *args, **kwargs)


class ListingDeleteView(DeleteView):
    model = None
    template_name = 'listing/listing_delete.html'
    success_url = reverse_lazy('listing_list')

    def dispatch(self, request, *args, **kwargs):
        self.model = {'push': Push, 'pull': Pull}.get(kwargs.get('type'))
        return DetailView.dispatch(self, request, *args, **kwargs)
