""" admin settings for listing module """
from django.contrib import admin
from .models import Push, Pull, Unit


class PushAdmin(admin.TabularInline):
    """ inline for push """
    model = Push


class PullAdmin(admin.TabularInline):
    """ inline for pull """
    model = Pull


class CategoryAdmin(admin.ModelAdmin):
    """ category admin """
    inlines = [PushAdmin, PullAdmin]


admin.site.register(Unit)
admin.site.register(Push)
admin.site.register(Pull)
