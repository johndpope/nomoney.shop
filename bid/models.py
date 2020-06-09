from django.db import models
from django.utils.timezone import now
from config.settings import AUTH_USER_MODEL


class BidPosition(models.Model):
    bid = models.ForeignKey(
        'Bid',
        on_delete=models.CASCADE,
        #related_name='listing_push_deals'
        )
    listing = models.ForeignKey(
        'listing.Listing',
        on_delete=models.CASCADE,
        #related_name='listing_push_deals'
        )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
        )
    unit = models.ForeignKey(
        'listing.Unit',
        on_delete=models.CASCADE,
        #related_name='unit_push_deals'
        )


class Bid(models.Model):
    positions = models.ManyToManyField(
        'listing.Listing',
        through='BidPosition',
        through_fields=('bid', 'listing'),
        )

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    datetime = models.DateTimeField(default=now, editable=False)
    deal = models.BooleanField(default=False)

    def add_position(self, listing, quantity, unit):
        import pdb; pdb.set_trace()  # <---------
