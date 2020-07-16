""" models of deal module """
from django.db import models
from django.db.models import Q
from feedback.models import PushFeedback, UserFeedback
from .deal_status import DealStatus
from .deal_base import DealBase


class Deal(DealBase):  # pylint: disable=too-many-public-methods
    """ deal is an exchange case """

    def set_accepted(self):
        """ set this deal status to accepted """
        self.status = DealStatus.ACCEPTED
        self.save()

    def set_placed(self):
        """ set this deal status to placed """
        self.status = DealStatus.PLACED
        self.save()

    def set_pov(self, pov_user):
        """ sets the pov_user ("point-of-view-user")
        :param pov_user: User that is the user that acesses the deal as main user
        :returns: self
        """
        self.pov_user = pov_user
        return self

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
        """ deal quality is calculated from the length of possible pushs and pulls
        :returns: int
        """
        if self._quality:
            return self._quality
        self._quality = len(self.pushs + self.pulls)
        return self._quality

    def get_users(self):
        """ users of this deal according to the point of view
        :returns: User(user), User(partner)
        """
        return self.user, self.partner

    def get_latest_bid(self):
        """ latest bid given to that deal
        :returns: Bid object or None
        """
        bids = self.bids
        return bids.latest() if bids else None

    def can_accept(self, user):
        """ calculates if a user has the right to accept that deal
        therefore he must not be the latest bid creator
        :param user: user to check rights of
        :returns: bool
        """
        latest_bid = self.get_latest_bid()
        if not latest_bid:
            return False
        if latest_bid.creator != user:
            return True
        return False

    def can_bid(self, user):
        """ calculates if a user has the right to bid to that deal
        therefore he must not be the latest bid creator
        :param user: user to check rights of
        :returns: bool
        """
        latest_bid = self.get_latest_bid()
        if not latest_bid:
            return True
        if latest_bid.creator != user:
            return True
        return False

    @classmethod
    def by_users(cls, user1, user2, create=False):
        """ get deals by users
        :param user1: User
        :param user2: User
        :param create: bool if deal should be created if not exist(default: False)
        :returns: QuerySet of deals
        """
        existing = cls.objects.filter(
            Q(user1=user1, user2=user2) |
            Q(user2=user1, user1=user2)
            )
        if create and not existing:
            deal = cls.objects.create(user1=user1, user2=user2)
            return cls.objects.filter(pk=deal.pk)
        return existing

    @classmethod
    def get_or_create(cls, *users):
        """ shortcut for by_users method
        :param *users: 2x User
        :returns: QuerySet of deals
        :raises AttributeError: len(users) must be 2
        """
        if len(users) != 2:
            raise AttributeError('A deal has exactly 2 users')
        return cls.by_users(*users, create=True)

    def _create_feedbacks(self):
        UserFeedback.objects.create(
            creator=self.user,
            user=self.partner,
            deal=self,
            )
        UserFeedback.objects.create(
            creator=self.partner,
            user=self.user,
            deal=self
            )

    def _iterate_bidpositions(self, bid):
        for bid_position in bid.positions:
            push = bid_position.push
            creator = self.user1 if self.user2 == push.user else self.user2
            PushFeedback.objects.create(
                push=push,
                creator=creator,
                deal=self
                )

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        models.Model.save(self, *args, **kwargs)
        if self.status == DealStatus.ACCEPTED:
            self._create_feedbacks()
            self._iterate_bidpositions(self.get_latest_bid())

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return set([self.user1, self.user2]) == set([other.user1, other.user2])

    def __hash__(self):
        return hash(self.pk)

    def __str__(self):
        return '{} vs. {}'.format(self.user1, self.user2)

