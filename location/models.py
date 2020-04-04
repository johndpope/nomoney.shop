from django.db import models
from config.settings import AUTH_USER_MODEL


class Location(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    lon = models.DecimalField(
        null=True, blank=True, max_digits=9, decimal_places=6
        )
    lat = models.DecimalField(
        null=True, blank=True, max_digits=9, decimal_places=6
        )
