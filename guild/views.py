from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls.base import reverse
from .models import Guild
from deal.models import VirtualDeal


class GuildListView(ListView):
    model = Guild


class GuildDetailView(DetailView):
    model = Guild

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        context['deals_2d'] = VirtualDeal.combinated(
            *self.object.users.all(),
            me_=self.request.user
            )
        return context


class GuildCreateView(CreateView):
    model = Guild
    fields = ['title', 'users']

    def get_form(self, form_class=None):
        form = CreateView.get_form(self, form_class=form_class)
        form.fields['users'].widget.attrs['class'] = 'chosen-select'
        form.fields['users'].widget.attrs['data-placeholder'] = \
            'Benutzer auswählen ...'
        return form

    def get_success_url(self):
        return reverse('guild_detail', args=(self.object.pk, ))


class GuildUpdateView(UpdateView):
    model = Guild
    fields = ['title', 'users']

    def get_form(self, form_class=None):
        form = UpdateView.get_form(self, form_class=form_class)
        form.fields['users'].widget.attrs['class'] = 'chosen-select'
        form.fields['users'].widget.attrs['data-placeholder'] = \
            'Benutzer auswählen ...'
        return form

    def get_success_url(self):
        return reverse('guild_detail', args=(self.object.pk, ))


class GuildDeleteView(DeleteView):
    model = Guild
    template_name = 'guild/guild_delete.html'

    def get_success_url(self):
        return reverse('guild_list')
