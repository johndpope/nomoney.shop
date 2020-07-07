from django.db import models
from config.settings import AUTH_USER_MODEL
from chat.models import Chat


class Market(models.Model):
    users = models.ManyToManyField(AUTH_USER_MODEL)
    chat = models.OneToOneField(
        'chat.Chat', null=True, blank=True, on_delete=models.CASCADE
        )
    title = models.CharField(max_length=20)

    location = models.ForeignKey(
        'location.Location', on_delete=models.CASCADE, blank=True, null=True
        )

    def save(self, *args, **kwargs):
        if not self.chat:
            self.chat = Chat.objects.create()
        return models.Model.save(self, *args, **kwargs)

    def __str__(self):
        return self.title #or ', '.join((str(user) for user in self.users.all()))
