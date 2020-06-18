from django import forms
from .models import Bid, BidPush, BidPull

BID_POSITION_FIELDS = ['quantity', 'unit']


class BidForm(forms.ModelForm):

    def __init__(self, partner, *args, **kwargs):
        self.partner = partner
        super().__init__(*args, **kwargs)

    class Meta:
        model = Bid
        fields = ['comment']


class BidPositionFormBase(forms.ModelForm):
    listing = None

    def __init__(self, listing, *args, **kwargs):
        self.listing = listing
        super().__init__(initial = {'unit': listing.unit.pk}, *args, **kwargs)


class BidPushForm(BidPositionFormBase, forms.ModelForm):

    class Meta:
        model = BidPush
        fields = BID_POSITION_FIELDS


class BidPullForm(BidPositionFormBase, forms.ModelForm):

    class Meta:
        model = BidPull
        fields = BID_POSITION_FIELDS
