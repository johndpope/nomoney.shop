from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator


class Unit(models.Model):
    name = models.CharField(max_length=50)


class Item(models.Model):
    count = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.01'))]
        )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE,)
