""" forms for the feedback module """
from django import forms
from .models import PushFeedback, UserFeedback


class PushFeedbackUpdateForm(forms.ModelForm):
    """ form for updating push feedbacks """

    class Meta:
        fields = ['score', 'subject', 'text']
        model = PushFeedback


class UserFeedbackUpdateForm(forms.ModelForm):
    """ form for updating push feedbacks """

    class Meta:
        fields = ['score', 'subject', 'text']
        model = UserFeedback
