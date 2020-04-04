from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from config.settings import AUTH_USER_MODEL


class Type(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()


class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class Review(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    score = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title


class Unit(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Listing(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    title = models.CharField(max_length=50)
    description = models.TextField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    count = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.01'))]
        )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
