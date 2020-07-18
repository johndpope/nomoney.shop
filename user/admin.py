""" admin settings for user module """
from django.contrib import admin
from .models import User


admin.site.register(User)
