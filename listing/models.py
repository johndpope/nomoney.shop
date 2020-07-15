from uuid import uuid4
from itertools import chain
from django.utils.translation import gettext_lazy as _
from django.db import models
from config.settings import AUTH_USER_MODEL
from chat.models import Chat
from statistics import mean


def image_path(instance, _):
    return 'listing/{}/{}'.format(instance.type, uuid4())


class ListingStatus(models.IntegerChoices):
    CREATED = 0, _('created')
    PAUSED = 10, _('paused')
    DELETED = 110, _('deleted')


class Unit(models.Model):
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
        return {'push': Pull, 'pull': Push}.get(self.type)

    def get_chat_with_partner(self, partner):
        return Chat.by_users(self.user, partner, create=True)

    def get_matches(self):
        cls = self.opposite_class
        return cls.objects.filter(category=self.category
                                  ).exclude(user=self.user)

    @staticmethod
    def get_all():
        return list(chain(Push.objects.all(), Pull.objects.all()))

    # pylint: disable=signature-differs, unused-argument
    def delete(self, *args, **kwargs):
        self.status = ListingStatus.DELETED
        self.save()

    def __hash__(self):
        return hash((self.pk, self.type))

    def __eq__(self, other):
        try:
            return self.category == other.category
        except AttributeError as e:
            print(e)

    def __str__(self):
        # pylint: disable=no-member
        return '{} {} {}'.format(self.user.username, self.type, self.title)

    class Meta:
        abstract = True


class Push(ListingBase):
    type = 'push'

    @property
    def score(self):
        scores = []
        for feedback in self.pushfeedback_set.all():
            if feedback.score:
                scores.append(feedback.score)
        if scores:
            return mean(scores)

    @property
    def feedbacks(self):
        return self.pushfeedback_set.all()

    class Meta:
        verbose_name = _('push')
        verbose_name_plural = _('pushs')


class Pull(ListingBase):
    type = 'pull'

    class Meta:
        verbose_name = _('pull')
        verbose_name_plural = _('pulls')
