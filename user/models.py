from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def pulls(self):
        return self.pull_set.all()

    @property
    def pushs(self):
        return self.push_set.all()


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    score = models.PositiveSmallIntegerField()
    subject = models.CharField(max_length=100)
    text = models.TextField()
