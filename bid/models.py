from django.db import models
from django.utils.timezone import now
from config.settings import AUTH_USER_MODEL


class BidPositionBase(models.Model):
    listing = None
    bid = models.ForeignKey(
        'Bid',
        on_delete=models.CASCADE,
        )
    quantity = models.PositiveIntegerField()
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


class StatusCode(models.IntegerChoices):
    UNSEEN = 0, 'unseen'
    SEEN = 10, 'seen'
    ACCEPTED = 20, 'accepted'
    ANSWERED = 30, 'answered'
    REJECTED = 40, 'rejected'


class Bid(models.Model):
    deal = models.ForeignKey('deal.Deal', on_delete=models.CASCADE)

    creator = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )

    datetime = models.DateTimeField(default=now, editable=False)

    status = models.PositiveSmallIntegerField(
        default=StatusCode.UNSEEN,
        choices=StatusCode.choices,
        )

    @property
    def pushs(self):
        return self.bidpush_set.all()

    @property
    def pulls(self):
        return self.bidpull_set.all()

    @property
    def is_latest(self):
        return self.get_latest() == self

    def get_latest(self):
        return self.deal.bid_set.latest()  # .order_by('datetime')

    def get_users(self):
        return self.deal.users.all()

    def same_constellation(self):
        print("Rework")
        return self.deal.bid_set.all()

    @classmethod
    def by_user(cls, user):
        return user.bid_set.all()

    def __lt__(self, other):
        return self.datetime < other.datetime

    class Meta:
        ordering = ['-datetime']
        get_latest_by = ['datetime']
