from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,\
    FormView
from django.urls.base import reverse_lazy
from .models import Push, Pull
from .forms import PushForm

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


class ListingCreateView(FormView):
    #model = None
    form_class = PushForm
    template_name = 'listing/listing_form.html'
    #fields = FIELDS
    success_url = reverse_lazy('listing_list')
    category = None

    def dispatch(self, request, *args, **kwargs):
        #self.model = {'push': Push, 'pull': Pull}.get(kwargs.get('type'))
        self.category = kwargs.get('category_pk', None)
        if self.category:
            self.initial['category'] = self.category
        return DetailView.dispatch(self, request, *args, **kwargs)

    def get_form(self):
        return self.form_class(request=self.request)

        #=======================================================================
        # title = form.cleaned_data.get('title')
        # image = form.cleaned_data.get('image')
        # category = form.cleaned_data.get('category')
        # quantity = form.cleaned_data.get('quantity')
        # unit = form.cleaned_data.get('unit')
        # description = form.cleaned_data.get('description')
        # user = self.request.user
        # self.model.objects.create(
        #     title=title,
        #     image=image,
        #     category=category,
        #     quantity=quantity,
        #     unit=unit,
        #     description=description,
        #     user=user
        #     )
        #=======================================================================


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
