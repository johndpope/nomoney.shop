""" forms of user module """
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from user.models import User


class CustomUserCreationForm(UserCreationForm):
    """ form for creating new user """

    class Meta(UserCreationForm.Meta):
        model = User


class CustomUserLoginForm(AuthenticationForm):
    """ form for users to login """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': '{} / {}'.format(
                _('email'),
                _('username'),
                ),
            'style': 'height:100%;'
            })
        self.fields['username'].label = ''

        self.fields['password'].widget.attrs.update({
            'placeholder': _('password'),
            'style': 'height:100%;'
            })
        self.fields['password'].label = ''
