from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from config.settings import AUTH_USER_MODEL
from chat.models import Chat, ChatType


class Market(models.Model):
    users = models.ManyToManyField(AUTH_USER_MODEL)
    title = models.CharField(max_length=20)
    location = models.ForeignKey(
        'location.Location', on_delete=models.CASCADE, blank=True, null=True
        )
    chat = None

    def save(self, *args, **kwargs):
        models.Model.save(self, *args, **kwargs)
        try:
            self.chat
        except ObjectDoesNotExist:
            self.chat = Chat.objects.create(
                type=ChatType.MARKET, market=self)

    def __str__(self):
        return self.title
