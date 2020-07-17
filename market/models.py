""" models for the market module """
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from config.settings import AUTH_USER_MODEL, LOGGER
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
        log_string = 'Market {}: title={} location={}'.format(
            'updated' if self.pk else 'created',
            str(self.title),
            str(self.location),
            )
        LOGGER.info(log_string)
        models.Model.save(self, *args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('market')
        verbose_name_plural = _('markets')


@receiver(post_save, sender=Market)
# pylint: disable=unused-argument
def create_chat(sender, instance, created, **kwargs):
    """ create market chat after creating market """
    if created:
        instance.chat = Chat.objects.create(
            type=ChatType.MARKET, market=instance)
        instance.save()
