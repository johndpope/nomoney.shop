from django.utils.translation import gettext_lazy as _
from django.db import models
from config.settings import AUTH_USER_MODEL


class FeedbackStatus(models.IntegerChoices):
    REQUEST = 0, _('request')
    SENT = 100, _('sent')
    CANCELED = 110, _('canceled')


class FeedbackBase(models.Model):
    creator = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('creator'),
        )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created'),
        )
    score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_('score'),
        )  # 0-100
    subject = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('subject'),
        )
    text = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('text'),
        )
    status = models.PositiveSmallIntegerField(
        default=FeedbackStatus.REQUEST,
        choices=FeedbackStatus.choices,
        verbose_name=_('status'),
        )
    deal = models.ForeignKey(
        'deal.Deal',
        on_delete=models.CASCADE,
        verbose_name=_('deal'),
        )
    type, push, user = 3 * [None]

    @property
    def object(self):
        return self.user or self.push

    @property
    def is_editable(self):
        return self.status == FeedbackStatus.REQUEST

    def set_sent(self):
        self.status = FeedbackStatus.SENT
        self.save()

    def __str__(self):
        return '{}: {}'.format(self.type, self.object)

    class Meta:
        abstract = True


class UserFeedback(FeedbackBase):
    type = 'user'
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedback_for',
        verbose_name=_('user'),
        )

    @classmethod
    def given_by_user(cls, user):
        return cls.objects.filter(creator__pk=user.pk)

    @classmethod
    def taken_by_user(cls, user):
        return cls.objects.filter(user__pk=user.pk)

    class Meta:
        verbose_name = _('userfeedback')
        verbose_name_plural = _('userfeedbacks')


class PushFeedback(FeedbackBase):
    type = 'push'
    push = models.ForeignKey('listing.Push', on_delete=models.CASCADE)

    @classmethod
    def given_by_user(cls, user):
        return cls.objects.filter(creator__pk=user.pk)

    @classmethod
    def taken_by_user(cls, user):
        return cls.objects.filter(push__user__pk=user.pk)

    class Meta:
        verbose_name = _('pushfeedback')
        verbose_name_plural = _('pushfeedbacks')
