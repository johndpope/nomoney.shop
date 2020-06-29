from django import forms
from .models import PushFeedback


class FeedbackCreateForm(forms.ModelForm):
    class Meta:
        fields = ['score', 'subject', 'text', 'push']
        model = PushFeedback
