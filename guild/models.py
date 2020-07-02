from django.db import models
from config.settings import AUTH_USER_MODEL
from chat.models import Chat


class Guild(models.Model):
    users = models.ManyToManyField(AUTH_USER_MODEL)
    chat = models.OneToOneField(
        'chat.Chat', null=True, blank=True, on_delete=models.CASCADE
        )
    title = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.chat:
            self.chat = Chat.objects.create()
        return models.Model.save(self, *args, **kwargs)
