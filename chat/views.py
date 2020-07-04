from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from .models import Chat
from .forms import ChatMessageForm


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat

    def get_queryset(self):
        return self.request.user.chat_set.all()


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    fields = '__all__'

    def get_context_data(self, **kwargs):
        kwargs['form'] = ChatMessageForm(self.request.POST)
        return DetailView.get_context_data(self, **kwargs)


class ChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    fields = '__all__'

    def get_success_url(self):
        return reverse('chat_detail', args=(self.object.pk,))


class ChatNewMessageView(LoginRequiredMixin, CreateView):
    form_class = ChatMessageForm

    def form_valid(self, form):
        chat_pk = self.request.resolver_match.kwargs.get('pk')
        form.instance.chat = Chat.objects.get(pk=chat_pk)
        form.instance.creator = self.request.user
        return CreateView.form_valid(self, form)

    def get_success_url(self):
        return reverse('chat_detail', args=(
            self.request.resolver_match.kwargs.get('pk'),
            ))


class ChatAjaxStatusView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):  # future?
        import pdb; pdb.set_trace()  # <---------
        return JsonResponse({'foo': 'bar'})
    

class ChatAjaxView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = 'chat/solo/chat_messages_ajax.html'
