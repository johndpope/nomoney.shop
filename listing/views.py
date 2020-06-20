from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls.base import reverse_lazy
from .models import Push, Pull

FIELDS = ['title', 'category', 'quantity', 'unit', 'description', 'image']
"""
listing_list - list pushs and pulls
listing_create
listing_update
listing_detail
"""


class ListingCreateView(CreateView):
    model = None
    template_name = 'listing/listing_form.html'
    fields = FIELDS
    success_url = reverse_lazy('listing_list')
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.model = {'push': Push, 'pull': Pull}.get(kwargs.get('type'))
        self.category = kwargs.get('category_id', None)
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

    def dispatch(self, request, *args, **kwargs):
        self.model = {'push': Push, 'pull': Pull}.get(kwargs.get('type'))
        return DetailView.dispatch(self, request, *args, **kwargs)


class ListingDeleteView(DeleteView):
    model = None
    template_name = 'listing/listing_delete.html'
    success_url = reverse_lazy('listing_list')

    def dispatch(self, request, *args, **kwargs):
        self.model = {'push': Push, 'pull': Pull}.get(kwargs.get('type'))
        return DetailView.dispatch(self, request, *args, **kwargs)
