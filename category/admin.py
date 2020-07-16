""" admin settings for category module """
from django.contrib import admin
from .models import Category


admin.site.register(Category)
