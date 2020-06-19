from django import forms
from .models import Bid, BidPush, BidPull

BID_POSITION_FIELDS = ['quantity', 'unit']


class BidForm(forms.ModelForm):

    def __init__(self, partner, *args, **kwargs):
        self.partner = partner
        super().__init__(*args, **kwargs)
        import pdb; pdb.set_trace()  # <---------

    class Meta:
        model = Bid
        exclude = ['user', 'partner', 'datetime', 'status']
        #fields = ['comment']


class BidPositionFormBase(forms.ModelForm):
    listing = None

    def __init__(self, listing, *args, **kwargs):
        self.listing = listing
        super().__init__(*args, **kwargs)

    def get_initial_for_field(self, field, field_name):
        if field_name == 'quantity':
            return 0
        elif field_name == 'unit':
            return self.listing.unit.pk


class BidPushForm(BidPositionFormBase, forms.ModelForm):

    class Meta:
        model = BidPush
        fields = BID_POSITION_FIELDS


class BidPullForm(BidPositionFormBase, forms.ModelForm):

    class Meta:
        model = BidPull
        fields = BID_POSITION_FIELDS
