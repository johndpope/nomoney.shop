from django import forms
from .models import Deal


class DealCreateForm(forms.ModelForm):

    class Meta:
        model = Deal
        fields = ['user2']


class DealAcceptForm(forms.ModelForm):

    class Meta:
        model = Deal
        fields = '__all__'
