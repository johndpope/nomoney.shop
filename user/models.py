from django.db import models
from django.contrib.auth.models import AbstractUser
from action.models import Action


class User(AbstractUser):
    pass