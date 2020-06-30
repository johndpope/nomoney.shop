from django.db import models
from django.utils.timezone import now
from config.settings import AUTH_USER_MODEL


class BidStatus(models.IntegerChoices):
    UNSEEN = 0, 'unseen'
    SEEN = 10, 'seen'
    ANSWERED = 30, 'answered'
    ACCEPTED = 100, 'accepted'
    REJECTED = 110, 'rejected'


class BidPosition(models.Model):
    push = models.ForeignKey('listing.Push', on_delete=models.CASCADE)
    bid = models.ForeignKey('Bid', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit = models.ForeignKey('listing.Unit', on_delete=models.CASCADE)

    @property
    def listing(self):
        return self.push


class Bid(models.Model):
    deal = models.ForeignKey('deal.Deal', on_delete=models.CASCADE)
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=now, editable=False)
    status = models.PositiveSmallIntegerField(
        default=BidStatus.UNSEEN,
        choices=BidStatus.choices,
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
