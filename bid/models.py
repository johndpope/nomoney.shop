""" models for bid module """
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils.timezone import now
from config.settings import AUTH_USER_MODEL


class BidStatus(models.IntegerChoices):
    """ This represents the status of each bid
    UNSEEN - New created bid, not seen by the partner
    SEEN - Bid was seen by the partner without any reaction
    ANSWERED - Partner answered the bid with a own bid
    ACCEPTED - Partner accepted the bid
    REJECTED - Partner rejected the bid
    """
    UNSEEN = 0, _('unseen')
    SEEN = 10, _('seen')
    ANSWERED = 30, _('answered')
    ACCEPTED = 100, _('accepted')
    REJECTED = 110, _('rejected')


class BidPosition(models.Model):
    """ A bid consists of multiple bid positions """
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
        """ Get the listing object (push) of this bid position """
        return self.push

    class Meta:
        verbose_name = _('bidposition')
        verbose_name_plural = _('bidpositions')


class Bid(models.Model):
    """ This is the bid that contains the bid positions """
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
        """ all positions of this bid
        :returns: QuerySet of bidposition objects
        """
        return self.bidposition_set.all()

    @property
    def pushs(self):
        """ Pushs of this user are pushs for the creator
        :returns: QuerySet of bidposition objects
        """
        return self.positions.filter(push__user=self.creator)

    @property
    def pulls(self):
        """ Pushs of other user are pulls for the creator
        :returns: QuerySet of bidposition objects
        """
        return self.positions.exclude(push__user=self.creator)

    @property
    def is_latest(self):
        """ True if this is the latest bid for this deal
        :returns: bool
        """
        return self.get_latest() == self

    def get_latest(self):
        """ Get the latest bid for this deal
        :returns: bid object
        """
        return self.deal.bid_set.latest()  # .order_by('datetime')

    def get_users(self):
        """ Get users that belong to this bid
        :returns: QuerySet of user objects
        """
        return self.deal.users.all()

    @classmethod
    def by_user(cls, user):
        """ Get bid by user
        :param user: User of which to get all bids
        :returns: QuerySet of bid objects
        """
        return user.bid_set.all()

    def __lt__(self, other):
        return self.datetime < other.datetime

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        super().save(*args, **kwargs)
        self.deal.set_placed()

    class Meta:
        ordering = ['-datetime']
        get_latest_by = ['datetime']
        verbose_name = _('bid')
        verbose_name_plural = _('bids')
