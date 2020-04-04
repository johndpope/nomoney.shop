from django.db import models
from django.contrib.auth.models import AbstractUser
from action.models import Pull, Push


class User(AbstractUser):
    pulls = models.ForeignKey(Pull, on_delete=models.CASCADE, null=True)
    pushs = models.ForeignKey(Push, on_delete=models.CASCADE, null=True)
