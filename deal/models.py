from django.db import models
from config.settings import AUTH_USER_MODEL


class Deal(models.Model):
    users = models.ManyToManyField(AUTH_USER_MODEL)


class SingleDeal(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    partner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partner'
        )
    accepted = models.BooleanField(default=False)
