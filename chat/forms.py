""" forms for the chat module """
from django import forms
from .models import ChatMessage


class ChatMessageForm(forms.ModelForm):
    """ form to create a new chat message """

    def get_initial_for_field(self, field, field_name):
        response = forms.ModelForm.get_initial_for_field(self, field, field_name)
        self.fields['text'].widget.attrs['rows'] = 2
        return response

    class Meta:
        model = ChatMessage
        fields = ['text']
