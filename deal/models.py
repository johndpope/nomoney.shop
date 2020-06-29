from django.db import models
from django.db.models import Q
from config.settings import AUTH_USER_MODEL


class DealStatus(models.IntegerChoices):
    VIRTUAL = 0, 'virtual'
    STARTED = 10, 'started'
    PLACED = 20, 'placed'
    ACCEPTED = 50, 'accepted'
    DELETED = 100, 'deleted'


class Deal(models.Model):
    user1 = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user1_deals'
        )
    user2 = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user2_deals'
        )
    guild = models.ForeignKey(
        'guild.Guild', on_delete=models.CASCADE, null=True, blank=True
        )
    status = models.PositiveSmallIntegerField(
        default=DealStatus.VIRTUAL,
        choices=DealStatus.choices,
        )

    pov_user = None

    _level = None
    _quality = None

    @property
    def accepted(self):
        return self.status == DealStatus.ACCEPTED

    @property
    def deleted(self):
        return self.status == DealStatus.DELETED

    @property
    def user(self):
        if self.pov_user == self.user2:
            return self.user2
        return self.user1

    @property
    def partner(self):
        if self.pov_user == self.user2:
            return self.user1
        return self.user2

    @property
    def bids(self):
        return self.bid_set.filter()

    @property
    def pushs(self):
        # pylint: disable=no-member
        return list(self.intersection(self.user.pushs, self.partner.pulls))

    @property
    def pulls(self):
        # pylint: disable=no-member
        return list(self.intersection(self.user.pulls, self.partner.pushs))

    @property
    def level(self):
        """ Levels:
            0 - No Deal match
            1 - One side Match
            2 - Two side Match
            3 - Deal between three users
            4 - Deal between four users
        users represent all users taking part at this deal
        """
        if self._level:
            return self._level
        level = 0
        if self.pushs:
            level += 1
        if self.pulls:
            level += 1
        self._level = level
        return self._level

    @property
    def quality(self):
        if self._quality:
            return self._quality
        self._quality = len(self.pushs + self.pulls)
        return self._quality

    def set_pov(self, me_):
        self.pov_user = me_

    def get_users(self):
        return self.user1, self.user2

    def get_latest_bid(self):
        bids = self.bids
        return bids.latest() if bids else None

    def can_accept(self, user):
        latest_bid = self.get_latest_bid()
        if not latest_bid:
            return False
        if latest_bid.creator != user:
            return True
        return False

    def can_bid(self, user):
        latest_bid = self.get_latest_bid()
        if not latest_bid:
            return True
        if latest_bid.creator != user:
            return True
        return False

    #===========================================================================
    # @classmethod
    # def by_user(cls, me_, partner):
    #     import pdb; pdb.set_trace()  # <---------
    #===========================================================================

    @classmethod
    def get_or_create(cls, users):
        existing = cls.objects.filter(
            Q(user1=users[0], user2=users[1]) |
            Q(user2=users[0], user1=users[1])
            )
        if existing:
            return existing.latest()
        return cls.objects.create(user1=users[0], user2=users[1])

    @staticmethod
    def intersection(lst1, lst2):
        """ returns intersecting elements """
        for element in lst1:
            if element in lst2:
                yield element

    class Meta:
        get_latest_by = ['pk']
