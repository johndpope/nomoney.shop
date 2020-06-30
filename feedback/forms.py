from django import forms
from .models import PushFeedback, UserFeedback


class PushFeedbackUpdateForm(forms.ModelForm):
    class Meta:
        fields = ['score', 'subject', 'text']
        model = PushFeedback


class UserFeedbackUpdateForm(forms.ModelForm):
    class Meta:
        fields = ['score', 'subject', 'text']
        model = UserFeedback
