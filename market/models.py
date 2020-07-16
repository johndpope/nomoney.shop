""" models for the market module """
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from config.settings import AUTH_USER_MODEL
from chat.models import Chat, ChatType


class Market(models.Model):
    """ a market is like a group of users that deal with each other """
    users = models.ManyToManyField(
        AUTH_USER_MODEL,
        verbose_name=_('users'),
        )
    title = models.CharField(
        max_length=20,
        verbose_name=_('title'),
        )
    location = models.ForeignKey(
        'location.Location',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('location'),
        )
    chat = None

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        models.Model.save(self, *args, **kwargs)
        try:
            self.chat
        except ObjectDoesNotExist:
            self.chat = Chat.objects.create(
                type=ChatType.MARKET, market=self)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('market')
        verbose_name_plural = _('markets')
