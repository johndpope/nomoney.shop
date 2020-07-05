from django.db import models
from config.settings import AUTH_USER_MODEL


class FeedbackStatus(models.IntegerChoices):
    REQUEST = 0
    SENT = 100
    CANCELED = 110


class FeedbackBase(models.Model):
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    score = models.PositiveSmallIntegerField(null=True, blank=True)  # 0-100
    subject = models.CharField(max_length=30, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        default=FeedbackStatus.REQUEST,
        choices=FeedbackStatus.choices,
        )
    deal = models.ForeignKey('deal.Deal', on_delete=models.CASCADE)
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
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_for'
        )

    @classmethod
    def given_by_user(cls, user):
        return cls.objects.filter(creator__pk=user.pk)

    @classmethod
    def taken_by_user(cls, user):
        return cls.objects.filter(user__pk=user.pk)


class PushFeedback(FeedbackBase):
    type = 'push'
    push = models.ForeignKey('listing.Push', on_delete=models.CASCADE)

    @classmethod
    def given_by_user(cls, user):
        return cls.objects.filter(creator__pk=user.pk)

    @classmethod
    def taken_by_user(cls, user):
        return cls.objects.filter(push__user__pk=user.pk)
