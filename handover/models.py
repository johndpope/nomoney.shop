from django.db import models
from location.models import Location


class Handover(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE,)
    title = models.CharField(max_length=100)
    description = models.TextField()
