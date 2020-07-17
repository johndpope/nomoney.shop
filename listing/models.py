""" models of the listing module """
from uuid import uuid4
from itertools import chain
from statistics import mean
from django.utils.translation import gettext_lazy as _
from django.db import models
from config.settings import AUTH_USER_MODEL, LOGGER
from chat.models import Chat


def image_path(instance, _):
    """ calculate the file path for listing images """
    return 'listing/{}/{}'.format(instance.type, uuid4())


class ListingStatus(models.IntegerChoices):
    """ Status of listings
    CREATED - normal status
    PAUSED - paused listing should be excluded from all calculations
    DELETED - deleted listing should be excluded from all calculations
    """
    CREATED = 0, _('created')
    PAUSED = 10, _('paused')
    DELETED = 110, _('deleted')


class Unit(models.Model):
    """ unit model """
    title = models.CharField(
        max_length=20,
        verbose_name=_('title'),
        )
    short = models.CharField(
        max_length=5,
        verbose_name=_('shorttitle'),
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('unit')
        verbose_name_plural = _('units')


class ListingBase(models.Model):
    """ Base model for listing types (push and pull) """
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        )
    title = models.CharField(
        max_length=50,
        verbose_name=_('title'),
        )
    category = models.ForeignKey(
        'category.Category',
        on_delete=models.CASCADE,
        verbose_name=_('category'),
        )
    quantity = models.PositiveIntegerField(
        verbose_name=_('quantity'),
        )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name=_('unit'),
        )
    image = models.ImageField(
        blank=True,
        upload_to=image_path,
        verbose_name=_('image'),
        )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('description'),
        )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created'),
        )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_('modified'),
        )
    location = models.ForeignKey(
        'location.Location',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('location'),
        )
    status = models.PositiveSmallIntegerField(
        default=ListingStatus.CREATED,
        choices=ListingStatus.choices,
        verbose_name=_('status'),
        )
    type = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._actions = {0: set(), 1: set(), 2: set(), 3: set()}

    @property
    def opposite_class(self):
        """
        :returns: Pull or Push class
        """
        return {'push': Pull, 'pull': Push}.get(self.type)

    def get_chat_with_partner(self, partner):
        """ get the listing related chat
        :param partner: User that want to chat about this listing
        :returns: Chat object
        """
        return Chat.by_users(self.user, partner, create=True)

    def get_matches(self):
        """ calculates matches for this listing
        :returns: QuerySet(Listing) while listing is Push or Pull object
        """
        cls = self.opposite_class
        return cls.objects.filter(category=self.category
                                  ).exclude(user=self.user)

    @staticmethod
    def get_all():
        """ gets all pushs and pulls
        :returns: list(Pushs + Pulls)
        """
        return list(chain(Push.objects.all(), Pull.objects.all()))

    # pylint: disable=signature-differs, unused-argument
    def delete(self, *args, **kwargs):
        """ when a listing is deleted, it will be only marked as DELETED """
        self.status = ListingStatus.DELETED
        self.save()

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        log_string = 'Listing {}: type={} user={} category={} quantity={}{} status={}'.format(
            'updated' if self.pk else 'created',
            str(self.type),
            str(self.user),
            str(self.category),
            str(self.quantity),
            str(self.unit.short),
            str(self.status),
            )
        LOGGER.info(log_string)
        super().save(*args, **kwargs)

    def __hash__(self):
        return hash((self.pk, self.type))

    def __eq__(self, other):
        try:
            return self.category == other.category
        except AttributeError as err:
            LOGGER.exception(err)

    def __str__(self):
        # pylint: disable=no-member
        return '{} {} {}'.format(self.user.username, self.type, self.title)

    class Meta:
        abstract = True


class Push(ListingBase):
    """ A push is a good or service that is provided to the network """
    type = 'push'

    @property
    def score(self):
        """ the score is calculated from the already given feedbacks
        :returns: int score or None
        """
        scores = []
        for feedback in self.pushfeedback_set.all():
            if feedback.score:
                scores.append(feedback.score)
        if scores:
            return mean(scores)
        return None

    @property
    def feedbacks(self):
        """
        :returns: all feedbacks for this push
        """
        return self.pushfeedback_set.all()

    class Meta:
        verbose_name = _('push')
        verbose_name_plural = _('pushs')


class Pull(ListingBase):
    """ A push is a good or service that is requested from the network """
    type = 'pull'

    class Meta:
        verbose_name = _('pull')
        verbose_name_plural = _('pulls')
