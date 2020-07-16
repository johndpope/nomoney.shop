""" forms of user module """
from django.contrib.auth.forms import UserCreationForm
from user.models import User


class CustomUserCreationForm(UserCreationForm):
    """ form for creating new user """

    class Meta(UserCreationForm.Meta):
        model = User
