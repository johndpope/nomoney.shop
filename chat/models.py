from django.db import models
from config.settings import AUTH_USER_MODEL


class ChatMessage(models.Model):
    chat = models.ForeignKey('chat.Chat', on_delete=models.CASCADE, )
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, )
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class Chat(models.Model):
    users = models.ManyToManyField(AUTH_USER_MODEL)
