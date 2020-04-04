from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    score = models.PositiveSmallIntegerField()
    subject = models.CharField(max_length=100)
    text = models.TextField()
