""" deal status """
from django.utils.translation import gettext_lazy as _
from django.db import models


class DealStatus(models.IntegerChoices):
    """ Status of a deal
    VIRTUAL - default, not used so far
    STARTET - deal is started
    PLACED - deal has placed bids
    ACCEPTED - deal is accepted
    CANCELED - deal is canceled
    """
    VIRTUAL = 0, _('virtual')
    STARTED = 10, _('started')
    PLACED = 20, _('placed')
    ACCEPTED = 100, _('accepted')
    CANCELED = 110, _('canceled')

    @property
    def choices(self):
        """ remove missing member error """
        super().choices()
