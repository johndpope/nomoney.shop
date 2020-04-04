from django.db import models
from config.settings import AUTH_USER_MODEL


class Action(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        )
    title = models.CharField(max_length=100)
    text = models.TextField()
