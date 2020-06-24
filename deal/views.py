from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from .models import DealSet
from django.urls.base import reverse


class DealListView(ListView):
    model = DealSet
    template_name = 'deal/deal_list.html'

    def get_queryset(self):
        return self.request.user.dealsets


class DealDetailView(DetailView):
    model = DealSet
    template_name = 'deal/deal_detail.html'


class DealCreateView(CreateView):
    model = DealSet
    fields = '__all__'

    def get_success_url(self):
        return reverse('deal_detail', args=(self.object.pk,))


class DealUpdateView(UpdateView):
    pass
