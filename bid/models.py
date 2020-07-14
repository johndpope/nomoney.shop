from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils.timezone import now
from config.settings import AUTH_USER_MODEL


class BidStatus(models.IntegerChoices):
    UNSEEN = 0, _('unseen')
    SEEN = 10, _('seen')
    ANSWERED = 30, _('answered')
    ACCEPTED = 100, _('accepted')
    REJECTED = 110, _('rejected')


class BidPosition(models.Model):
    push = models.ForeignKey(
        'listing.Push',
        on_delete=models.CASCADE,
        verbose_name=_('push'),
        )
    bid = models.ForeignKey(
        'Bid',
        on_delete=models.CASCADE,
        verbose_name=_('bid'),
        )
    quantity = models.PositiveIntegerField(
        verbose_name=_('quantity'),
        )
    unit = models.ForeignKey(
        'listing.Unit',
        on_delete=models.CASCADE,
        verbose_name=_('unit'),
        )

    @property
    def listing(self):
        return self.push

    class Meta:
        verbose_name = _('bidposition')
        verbose_name_plural = _('bidpositions')


class Bid(models.Model):
    deal = models.ForeignKey(
        'deal.Deal',
        on_delete=models.CASCADE,
        verbose_name=_('deal'),
        )
    creator = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('creator'),
        )
    datetime = models.DateTimeField(
        default=now,
        editable=False,
        verbose_name=_('time'),
        )
    status = models.PositiveSmallIntegerField(
        default=BidStatus.UNSEEN,
        choices=BidStatus.choices,
        verbose_name=_('status'),
        )

    @property
    def positions(self):
        return self.bidposition_set.all()

    @property
    def pushs(self):
        return self.positions.filter(push__user=self.creator)

    @property
    def pulls(self):
        return self.positions.exclude(push__user=self.creator)

    @property
    def is_latest(self):
        return self.get_latest() == self

    def get_latest(self):
        return self.deal.bid_set.latest()  # .order_by('datetime')

    def get_users(self):
        return self.deal.users.all()

    @classmethod
    def by_user(cls, user):
        return user.bid_set.all()

    def __lt__(self, other):
        return self.datetime < other.datetime

    class Meta:
        ordering = ['-datetime']
        get_latest_by = ['datetime']
        verbose_name = _('bid')
        verbose_name_plural = _('bids')
