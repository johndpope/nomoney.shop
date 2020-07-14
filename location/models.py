from django.utils.translation import gettext_lazy as _
from django.db import models
from config.settings.base import AUTH_USER_MODEL


class Location(models.Model):
    title = models.CharField(
        max_length=20,
        verbose_name=_('title'),
        )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        )
    lon = models.DecimalField(
        default=0.0,
        max_digits=10,
        decimal_places=7,
        verbose_name=_('longitude'),
        )
    lat = models.DecimalField(
        default=0.0,
        max_digits=10,
        decimal_places=7,
        verbose_name=_('latitude'),
        )
    description = models.TextField(
        blank=True,
        verbose_name=_('description'),
        )
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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
