from datetime import datetime
from django.db import models
from config.settings import AUTH_USER_MODEL
from django.utils.timezone import now


class Bid(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    push_listing = models.ForeignKey(
        'listing.Listing',
        on_delete=models.CASCADE,
        related_name='listing_push_deals'
        )
    push_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
        )
    push_unit = models.ForeignKey(
        'listing.Unit',
        on_delete=models.CASCADE,
        related_name='unit_push_deals'
        )
    pull_listing = models.ForeignKey(
        'listing.Listing',
        on_delete=models.CASCADE,
        related_name='listing_pull_deals'
        )
    pull_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    pull_unit = models.ForeignKey(
        'listing.Unit',
        on_delete=models.CASCADE,
        related_name='unit_pull_deals'
        )
    datetime = models.DateTimeField(default=now, editable=False)
    deal = models.BooleanField(default=False)

    #===========================================================================
    # @property
    # def user(self):
    #     return self.push_listing.user
    #===========================================================================
