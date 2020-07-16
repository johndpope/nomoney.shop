""" forms for the bid module """
from django import forms
from .models import BidPosition

BID_POSITION_FIELDS = ['quantity', 'unit']


class BidForm(forms.Form):
    """ Form for creating new bid """
    def __init__(self, listings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listings = listings
        for listing in self.listings:
            key = '_' + listing.type + '_' + str(listing.pk)
            self.fields['quantity' + key] = forms.IntegerField(
                min_value=0, required=False
                )
            field = self.fields['quantity' + key]
            field.listing = listing
            field.unit = listing.unit
            field.label = '{} ({})'.format(listing.title, listing.unit)
            field.widget.attrs['class'] = 'list-group-item data-slider '
            field.widget.attrs['data-slider-id'] = 'quantity' + key
            field.widget.attrs['data-slider-min'] = '0'
            field.widget.attrs['data-slider-max'] = listing.quantity
            field.widget.attrs['data-slider-step'] = '1'
            field.widget.attrs['data-slider-value'] = '0'

    def full_clean(self):
        return forms.Form.full_clean(self)


class BidPositionFormBase(forms.ModelForm):
    """ Base Form for creating different bid positions """
    def __init__(self, deal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.deal = deal


    def save(self, bid, commit=True):  # pylint: disable=arguments-differ
        self.instance.bid = bid
        return forms.ModelForm.save(self, commit=commit)


class BidPushForm(BidPositionFormBase, forms.ModelForm):
    """ Form for creating push bid positions """

    class Meta:
        model = BidPosition
        fields = BID_POSITION_FIELDS


class BidPullForm(BidPositionFormBase, forms.ModelForm):
    """ Form for creating pull bid positions """

    class Meta:
        model = BidPosition
        fields = BID_POSITION_FIELDS
