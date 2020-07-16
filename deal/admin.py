""" admin settings for deal module """
from django.contrib import admin
from .models import Deal


admin.site.register(Deal)
