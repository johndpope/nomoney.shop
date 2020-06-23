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
        return ', '.join((str(user) for user in self.users.all()))

    @property
    def messages(self):
        return self.chatmessage_set.all()
