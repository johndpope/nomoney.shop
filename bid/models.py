from django.db import models
from django.utils.timezone import now
from config.settings import AUTH_USER_MODEL


class BidPosition(models.Model):
    bid = models.ForeignKey(
        'Bid',
        on_delete=models.CASCADE,
        )
    listing = models.ForeignKey(
        'listing.Listing',
        on_delete=models.CASCADE,
        )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
        )
    unit = models.ForeignKey(
        'listing.Unit',
        on_delete=models.CASCADE,
        )


class StatusCode(models.IntegerChoices):
    UNSEEN = 0, 'unseen'
    SEEN = 10, 'seen'
    ACCEPTED = 20, 'accepted'
    ANSWERED = 30, 'answered'
    REJECTED = 40, 'rejected'


class Bid(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = 'bids_sent'
        )

    partner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = 'bids_received'
        )

    datetime = models.DateTimeField(default=now, editable=False)

    status = models.PositiveSmallIntegerField(
        default=StatusCode.UNSEEN,
        choices = StatusCode.choices,
        #validators=[status_validator]
        )

    comment = models.TextField(default='')
