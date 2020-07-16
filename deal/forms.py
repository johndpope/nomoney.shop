""" forms for deal module """
from django import forms
from .models import Deal


class DealCreateForm(forms.ModelForm):
    """ form for creating new deal """

    class Meta:
        model = Deal
        fields = ['user2', 'location']


class DealAcceptForm(forms.ModelForm):
    """ form for accepting deal """

    class Meta:
        model = Deal
        fields = '__all__'
