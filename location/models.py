from django.db import models
from config.settings.base import AUTH_USER_MODEL
from chat.models import Chat, ChatType


class Location(models.Model):
    title = models.CharField(max_length=20)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    lon = models.DecimalField(default=0.0, max_digits=10, decimal_places=7)
    lat = models.DecimalField(default=0.0, max_digits=10, decimal_places=7)
    description = models.TextField(blank=True)
    chat = None

    @property
    def deals(self):
        return self.deal_set.all()

    @property
    def markets(self):
        return self.market_set.all()

    @property
    def pushs(self):
        return self.push_set.all()

    @property
    def pulls(self):
        return self.pull_set.all()

    def save(self, *args, **kwargs):
        models.Model.save(self, *args, **kwargs)
        if not self.chat:
            self.chat = Chat.objects.create(
                type=ChatType.LOCATION, location=self)

    def __str__(self):
        return self.title
