from django.db import models
from config.settings import AUTH_USER_MODEL


class ChatMessage(models.Model):
    chat = models.ForeignKey('chat.Chat', on_delete=models.CASCADE, )
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, )
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ['-pk']


class Chat(models.Model):
    users = models.ManyToManyField(AUTH_USER_MODEL)

    @property
    def title(self):
        if self.users.all():
            return ', '.join((str(user) for user in self.users.all()))
        return 'Chat: {}'.format(self.pk)

    @property
    def messages(self):
        return self.chatmessage_set.all()

    @classmethod
    def by_users(cls, *user_list, create=False, virtual=False):
        chats = cls.objects.all()
        for chat in chats:
            if set(chat.users.all()) == set(user_list):
                return chat

        if create:
            chat = cls.objects.create()
            for user in user_list:
                chat.users.add(user)
            chat.save()
            return chat

        return None

    def __str__(self):
        return self.title
