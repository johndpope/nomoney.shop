from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from user.models import Feedback


admin.site.register(User, UserAdmin)
admin.site.register(Feedback)
