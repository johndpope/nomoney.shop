from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls.base import reverse
from .models import Chat
from .forms import ChatMessageForm


class ChatListView(ListView):
    model = Chat

    def get_queryset(self):
        return self.request.user.chat_set.all()


class ChatDetailView(DetailView):
    model = Chat
    fields = '__all__'

    def get_context_data(self, **kwargs):
        kwargs['form'] = ChatMessageForm(self.request.POST)
        return DetailView.get_context_data(self, **kwargs)


class ChatCreateView(CreateView):
    model = Chat
    fields = '__all__'

    def get_success_url(self):
        return reverse('chat_detail', args=(self.object.pk,))


class ChatNewMessageView(CreateView):
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
