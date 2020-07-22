""" models for the location module """
from django.utils.translation import gettext_lazy as _
from django.db import models
from config.settings import AUTH_USER_MODEL, LOGGER
from action.models import create_action


class Location(models.Model):
    """ a location can be a location of push, pull or market (later deal) """
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
        """ Deals of this location
        :returns: QuerySet(Deal)
        """
        return self.deal_set.all()

    @property
    def markets(self):
        """ markets of this location
        :returns: QuerySet(Market)
        """
        return self.market_set.all()

    @property
    def pushs(self):
        """ pushs of this location
        :returns: QuerySet(Push)
        """
        return self.push_set.all()

    @property
    def pulls(self):
        """ pulls of this location
        :returns: QuerySet(Pull)
        """
        return self.pull_set.all()

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        log_string = 'Location {}: title={} user={} lon={} lat={}'.format(
            'updated' if self.pk else 'created',
            str(self.title),
            str(self.user),
            str(self.lon),
            str(self.lat),
            )
        LOGGER.info(log_string)
        if not create_action(self.user, 'FIRST_LOCATION_CREATED'):
            create_action(self.user, 'LOCATION_CREATED')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
