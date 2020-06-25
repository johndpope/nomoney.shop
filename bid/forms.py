from django import forms
from .models import Bid, BidPush, BidPull
#from listing.models import Unit

BID_POSITION_FIELDS = ['quantity', 'unit']

class BidForm(forms.Form):
    
    def __init__(self, listings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listings = listings
        for listing in self.listings:
            key = '_' + listing.type + '_' + str(listing.pk)
            self.fields['quantity' + key] = forms.IntegerField(min_value=0, required=False)
            self.fields['quantity' + key].listing = listing
            self.fields['quantity' + key].unit = listing.unit
            self.fields['quantity' + key].label = listing.title

    def as_table(self):
        return forms.Form.as_table(self)

class BidPositionFormBase(forms.ModelForm):

    def __init__(self, deal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.deal = deal


    def save(self, bid, commit=True):
        self.instance.bid = bid
        return forms.ModelForm.save(self, commit=commit)


class BidPushForm(BidPositionFormBase, forms.ModelForm):

    class Meta:
        model = BidPush
        fields = BID_POSITION_FIELDS


class BidPullForm(BidPositionFormBase, forms.ModelForm):

    class Meta:
        model = BidPull
        fields = BID_POSITION_FIELDS
