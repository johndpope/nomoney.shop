from django import forms
from user.models import User
from .models import Deal
USER_CHOICES = [[user, user] for user in User.objects.all()]


class DealCreateForm(forms.ModelForm):

    class Meta:
        model = Deal
        fields = ['user2']


class DealAcceptForm(forms.ModelForm):
    
    class Meta:
        model = Deal
        fields = ['accepted']