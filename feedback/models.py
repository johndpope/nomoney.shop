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

    class Meta:
        abstract = True


class UserFeedback(FeedbackBase):
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_for'
        )


class PushFeedback(FeedbackBase):
    push = models.ForeignKey('listing.Push', on_delete=models.CASCADE)
