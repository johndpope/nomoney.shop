from django.db import models
from django.utils.timezone import now
from config.settings import AUTH_USER_MODEL
from enum import Enum


class BidPositionBase(models.Model):
    listing = None

    @property
    def push(self):
        return self.listing

    @property
    def pull(self):
        return self.listing

    bid = models.ForeignKey(
        'Bid',
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

    class Meta:
        abstract = True


class BidPush(BidPositionBase):
    listing = models.ForeignKey(
        'listing.Push',
        on_delete=models.CASCADE,
        )


class BidPull(BidPositionBase):
    listing = models.ForeignKey(
        'listing.Pull',
        on_delete=models.CASCADE,
        )


class StatusCode():
    UNSEEN = 0, 'unseen'
    SEEN = 10, 'seen'
    ACCEPTED = 20, 'accepted'
    ANSWERED = 30, 'answered'
    REJECTED = 40, 'rejected'

    @classmethod
    def choices(cls):
        return (cls.UNSEEN, cls.SEEN, cls.ACCEPTED, cls.ANSWERED, cls.REJECTED)


class Bid(models.Model):
    pushs = models.ManyToManyField(
        'listing.Push',
        through=BidPush,
        through_fields=('bid', 'listing'),
        )

    pulls = models.ManyToManyField(
        'listing.Pull',
        through=BidPull,
        through_fields=('bid', 'listing'),
        )

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bids_sent',
        )

    partner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = 'bids_received',
        )

    datetime = models.DateTimeField(default=now, editable=False)

    status = models.PositiveSmallIntegerField(
        default=StatusCode.UNSEEN[0],
        choices = StatusCode.choices(),
        #validators=[status_validator]
        )

    comment = models.TextField(default='', blank=True)

    @property
    def push_positions(self):
        return self.bidpush_set.all()

    @property
    def pull_positions(self):
        return self.bidpull_set.all()
