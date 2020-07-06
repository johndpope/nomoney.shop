from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls.base import reverse
from .models import Guild
from deal.models import VirtualDeal
from django.contrib.auth.mixins import LoginRequiredMixin


class GuildListView(LoginRequiredMixin, ListView):
    model = Guild
    context_object_name = 'guilds'

    def get_queryset(self):
        return self.request.user.guild_set.all()


class GuildDetailView(LoginRequiredMixin, DetailView):
    model = Guild

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        context['deals_2d'] = VirtualDeal.combinated(
            *self.object.users.all(),
            me_=self.request.user
            )
        context['chat'] = self.object.chat
        return context


class GuildCreateView(LoginRequiredMixin, CreateView):
    model = Guild
    fields = ['title', 'users', 'location']

    def get_form(self, form_class=None):
        form = CreateView.get_form(self, form_class=form_class)
        form.fields['users'].widget.attrs['class'] = 'chosen-select'
        form.fields['users'].widget.attrs['data-placeholder'] = \
            'Benutzer auswählen ...'
        form.fields['users'].queryset = form.fields['users'].queryset.exclude(
            pk=self.request.user.pk)
        return form

    def form_valid(self, form):
        response = CreateView.form_valid(self, form)
        form.instance.users.add(self.request.user)
        form.instance.save()
        return response

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class GuildUpdateView(LoginRequiredMixin, UpdateView):
    model = Guild
    fields = ['title', 'users', 'location']

    def get_form(self, form_class=None):
        form = UpdateView.get_form(self, form_class=form_class)
        form.fields['users'].widget.attrs['class'] = 'chosen-select'
        form.fields['users'].widget.attrs['data-placeholder'] = \
            'Benutzer auswählen ...'
        form.fields['users'].queryset = form.fields['users'].queryset.exclude(
            pk=self.request.user.pk)
        return form

    def form_valid(self, form):
        response = UpdateView.form_valid(self, form)
        form.instance.users.add(self.request.user)
        form.instance.save()
        return response

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))


class GuildDeleteView(LoginRequiredMixin, DeleteView):
    model = Guild
    template_name = 'guild/guild_delete.html'

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))
