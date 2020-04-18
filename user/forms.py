from django.contrib.auth.forms import UserCreationForm as _UserCreationForm,\
    AuthenticationForm
from django.contrib.auth import get_user_model
from user.models import User


class UserCreationForm(_UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
