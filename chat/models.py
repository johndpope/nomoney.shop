from django.db import models
from config.settings import AUTH_USER_MODEL


class Chat(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='own_chats')
    users = models.ManyToManyField(AUTH_USER_MODEL)
    title = models.CharField(max_length=50)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='own_message')
    shown = models.ManyToManyField(AUTH_USER_MODEL, related_name='shown_message')
    title = models.CharField(max_length=50)
    text = models.TextField()
