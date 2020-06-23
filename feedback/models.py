from django.db import models
from config.settings import AUTH_USER_MODEL


class FeedbackBase(models.Model):
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    score = models.PositiveSmallIntegerField()
    subject = models.CharField(max_length=30)
    text = models.TextField()

    class Meta:
        abstract = True


class UserFeedback(FeedbackBase):
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_for'
        )


class PushFeedback(FeedbackBase):
    push = models.ForeignKey('listing.Push', on_delete=models.CASCADE)
