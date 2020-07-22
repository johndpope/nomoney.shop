""" models of deal module """
from django.utils.translation import gettext_lazy as _
from django.db import models
from snakelib.iterable import intersection
from config.settings import AUTH_USER_MODEL, LOGGER
from chat.models import Chat
from .deal_status import DealStatus
from action.models import create_action


class DealBase(models.Model):
    """ Abstract model for Deal
    It should only contain the getters of the deal attributes
    """
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
        try:
            return list(intersection(self.user.pushs, self.partner.pulls))
        except AttributeError as err:
            LOGGER.exception(err)

    @property
    def pulls(self):
        """ pulls of this deal
        :returns: list of intersecting pulls of pov_user
        """
        # pylint: disable=no-member
        return list(intersection(self.user.pulls, self.partner.pushs))

    @property
    def partner_pushs(self):
        """ pushs of this deal
        :returns: list of intersecting pushs of pov_user's partner
        """
        # pylint: disable=no-member
        return list(intersection(self.partner.pushs, self.user.pulls))

    @property
    def partner_pulls(self):
        """ pulls of this deal
        :returns: list of intersecting pulls of pov_user's partner
        """
        # pylint: disable=no-member
        return list(intersection(self.partner.pulls, self.user.pushs))

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        log_string = 'Deal {}: user1={} user2={} market={} status={} location={}'.format(
            'updated' if self.pk else 'created',
            str(self.user1),
            str(self.user2),
            str(self.market),
            str(self.status),
            str(self.location),
            )
        LOGGER.info(log_string)
        create_action(self.user, 'DEAL_CREATED')
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        get_latest_by = ['pk']
        verbose_name = _('deal')
        verbose_name_plural = _('deals')
