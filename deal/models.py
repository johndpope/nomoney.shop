""" models of deal module """
from itertools import combinations
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Q
from config.settings import AUTH_USER_MODEL
from feedback.models import PushFeedback, UserFeedback
from chat.models import Chat


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


class Deal(models.Model):  # pylint: disable=too-many-public-methods
    """ deal is an exchange case """
    user1 = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user1_deals',
        verbose_name=_('user'),
        )
    user2 = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user2_deals',
        verbose_name=_('user'),
        )
    market = models.ForeignKey(
        'market.Market',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('market'),
        )
    status = models.PositiveSmallIntegerField(
        default=DealStatus.STARTED,
        choices=DealStatus.choices,
        verbose_name=_('status'),
        )
    location = models.ForeignKey(
        'location.Location',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('location'),
        )

    pov_user = None  # "point-of-view-user"
    _level = None
    _quality = None

    def set_accepted(self):
        """ set this deal status to accepted """
        self.status = DealStatus.ACCEPTED
        self.save()

    def set_placed(self):
        """ set this deal status to placed """
        self.status = DealStatus.PLACED
        self.save()

    @property
    def user(self):
        """ return the user of this deal. it recognizes pov_user
        :returns: User1 or pov_user
        """
        if self.pov_user and self.pov_user == self.user2:
            return self.user2
        return self.user1

    @property
    def partner(self):
        """ return the partner of this deal. it recognizes pov_user
        :returns: User2 or not pov_user
        """
        if self.user == self.user2:
            return self.user1
        return self.user2

    def set_pov(self, pov_user):
        """ sets the pov_user ("point-of-view-user")
        :param pov_user: User that is the user that acesses the deal as main user
        :returns: self
        """
        self.pov_user = pov_user
        return self

    @property
    def chat(self):
        """ returns the chat according to the users
        :returns: Chat object of user1 and user2
        """
        return Chat.by_users(self.user1, self.user2, create=True)

    @property
    def bids(self):
        """ bids for this deal
        :returns: Bid object
        """
        return self.bid_set.all()

    @property
    def pushs(self):
        """ pushs of this deal
        :returns: list of intersecting pushs of pov_user
        """
        # pylint: disable=no-member
        return list(self.intersection(self.user.pushs, self.partner.pulls))

    @property
    def pulls(self):
        """ pulls of this deal
        :returns: list of intersecting pulls of pov_user
        """
        # pylint: disable=no-member
        return list(self.intersection(self.user.pulls, self.partner.pushs))

    @property
    def partner_pushs(self):
        """ pushs of this deal
        :returns: list of intersecting pushs of pov_user's partner
        """
        # pylint: disable=no-member
        return list(self.intersection(self.partner.pushs, self.user.pulls))

    @property
    def partner_pulls(self):
        """ pulls of this deal
        :returns: list of intersecting pulls of pov_user's partner
        """
        # pylint: disable=no-member
        return list(self.intersection(self.partner.pulls, self.user.pushs))

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
        #=======================================================================
        # if len(users) != 2:
        #     raise AttributeError('A deal has exactly 2 users')
        #=======================================================================
        return cls.by_users(*users, create=True)

    @staticmethod
    def intersection(lst1, lst2):
        """ method to calculate intersection between two lists
        :param lst1: first list to user
        :param lst2: second list to user
        :yields: intersecting list elements
        """
        for element in lst1:
            if element in lst2:
                yield element

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        models.Model.save(self, *args, **kwargs)
        if self.status == DealStatus.ACCEPTED:
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
            bid = self.get_latest_bid()
            for bid_position in bid.positions:
                push = bid_position.push
                creator = self.user1 if self.user2 == push.user else self.user2
                PushFeedback.objects.create(
                    push=push,
                    creator=creator,
                    deal=self
                    )

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return set([self.user1, self.user2]) == set([other.user1, other.user2])

    def __hash__(self):
        return hash(self.pk)

    def __str__(self):
        return '{} vs. {}'.format(self.user1, self.user2)

    class Meta:
        get_latest_by = ['pk']
        verbose_name = _('deal')
        verbose_name_plural = _('deals')


class VirtualDeal(Deal):
    """ proxy model for deal to calculate deals that not (need to) exist """
    status = 0

    @classmethod
    def combinated(cls, *users, me_=None):
        """ get possible deal combinations of users
        :param *users: users, deals should be created for
        :param me_: User as point of view
        :returns: list of deals
        """
        deals = []
        for user1, user2 in combinations(users, 2):
            if user1 and user2:
                if me_ and user2 == me_:
                    user1, user2 = user2, user1
                deals.append(cls.by_user(user1, user2, level=0))
        return deals

    @classmethod
    def by_users(cls, me_, other_users, level=2):  # pylint: disable=arguments-differ
        """ get deal between me_ and other_users
        :param me_: User as point of view
        :param other_users: users, deals should be created for
        :param level: int of deal level you want to get (default: 2)
        :returns: list of deals, sorted by quality
        """
        deals = []
        # Calculate possible Deals
        for user in other_users:
            deal = cls(user1=me_, user2=user)
            if deal.level >= level:
                deals.append(deal)

        # Calculate max Quality
        max_quality = max(
            (deal.quality for deal in deals)
            ) if deals else 0

        # Calculate Quality Percentage of each deal (for view/css)
        for deal in deals:
            deal.max_quality = max_quality
            if max_quality == 0:
                deal.quality_pct = 100
            else:
                deal.quality_pct = int(deal.quality / max_quality * 100 + 0.5)

        return sorted(deals, key=lambda x: x.quality, reverse=True)

    @classmethod
    def by_user(cls, me_, partner, level=2):
        """ get deal between me_ and partner
        :param me_: User as point of view
        :param partner: deal partner
        :param level: int of deal level you want to get (default: 2)
        :returns: list of deals, sorted by quality
        """
        deals = cls.by_users(me_, [partner], level=level)
        return deals[0] if deals else None

    def save(self):  # pylint: disable=arguments-differ
        pass

    class Meta:
        proxy = True
