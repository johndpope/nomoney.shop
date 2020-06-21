from itertools import chain
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls.base import reverse_lazy
from .models import Push, Pull

FIELDS = ['title', 'image', 'category', 'quantity', 'unit', 'description']
"""
listing_list - list pushs and pulls
listing_create
listing_update
listing_detail
"""
class ListingListView(ListView):
    template_name = 'listing/listing_list.html'

    def dispatch(self, request, *args, **kwargs):
        return DetailView.dispatch(self, request, *args, **kwargs)

    def get_queryset(self):
        return Push.get_all()


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
    template_name = 'listing/listing_form.html'
    fields = FIELDS
    success_url = reverse_lazy('listing_list')
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.model = {'push': Push, 'pull': Pull}.get(kwargs.get('type'))
        self.category = kwargs.get('category_pk', None)
        if self.category:
            self.initial['category'] = self.category#Category.objects.get(category=self.category+1)
        return DetailView.dispatch(self, request, *args, **kwargs)


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
