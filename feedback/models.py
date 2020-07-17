""" models for feedback module """
from django.utils.translation import gettext_lazy as _
from django.db import models
from config.settings import AUTH_USER_MODEL, LOGGER


class FeedbackStatus(models.IntegerChoices):
    """ Status of a feedback
    REQUEST - Feedback created by system when finishing a deal
    SENT - Requested feedback was created by user
    CANCELED - Requested feedback was canceled by user
    """
    REQUEST = 0, _('request')
    SENT = 100, _('sent')
    CANCELED = 110, _('canceled')


class FeedbackBase(models.Model):
    """ base class for all kind of feedback """
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
        """ returns the object the feedback was created for
        :returns: User or Push object
        """
        return self.user or self.push

    @property
    def is_editable(self):
        """ calculates if the feedback is editable
        :returns: bool
        """
        return self.status == FeedbackStatus.REQUEST

    def set_sent(self):
        """ set the status to FeedbackStatus.SENT """
        self.status = FeedbackStatus.SENT
        self.save()

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        log_string = 'Feedback {}: type={} creator={} object={} score={} status={}'.format(
            'updated' if self.pk else 'created',
            str(self.type),
            str(self.creator),
            str(self.object),
            str(self.score),
            str(self.status),
            )
        LOGGER.info(log_string)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}: {}'.format(self.type, self.object)

    class Meta:
        abstract = True


class UserFeedback(FeedbackBase):
    """ Feedback for a user """
    type = 'user'
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedback_for',
        verbose_name=_('user'),
        )

    @classmethod
    def given_by_user(cls, user):
        """ userfeedbacks given by user
        :param user: User to fetch feedbacks of
        :returns: QuerySet(UserFeedback)
        """
        return cls.objects.filter(creator__pk=user.pk)

    @classmethod
    def taken_by_user(cls, user):
        """ userfeedbacks taken by user
        :param user: User to fetch feedbacks of
        :returns: QuerySet(UserFeedback)
        """
        return cls.objects.filter(user__pk=user.pk)

    class Meta:
        verbose_name = _('userfeedback')
        verbose_name_plural = _('userfeedbacks')


class PushFeedback(FeedbackBase):
    """ Feedback for a push """
    type = 'push'
    push = models.ForeignKey('listing.Push', on_delete=models.CASCADE)

    @classmethod
    def given_by_user(cls, user):
        """ pushfeedbacks given by user
        :param user: User to fetch feedbacks of
        :returns: QuerySet(PushFeedback)
        """
        return cls.objects.filter(creator__pk=user.pk)

    @classmethod
    def taken_by_user(cls, user):
        """ pushfeedbacks taken by user
        :param user: User to fetch feedbacks of
        :returns: QuerySet(PushFeedback)
        """
        return cls.objects.filter(push__user__pk=user.pk)

    class Meta:
        verbose_name = _('pushfeedback')
        verbose_name_plural = _('pushfeedbacks')
