from django.contrib import admin
from .models import Push, Pull, Unit


class PushAdmin(admin.TabularInline):
    model = Push


class PullAdmin(admin.TabularInline):
    model = Pull


class CategoryAdmin(admin.ModelAdmin):
    inlines = [PushAdmin, PullAdmin]


admin.site.register(Unit)
admin.site.register(Push)
admin.site.register(Pull)
