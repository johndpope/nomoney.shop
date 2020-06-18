from django.contrib import admin
from .models import Category, Push, Pull, Review, Unit


class PushAdmin(admin.TabularInline):
    model = Push


class PullAdmin(admin.TabularInline):
    model = Pull


class CategoryAdmin(admin.ModelAdmin):
    inlines = [PushAdmin, PullAdmin]


#admin.site.register(Push)
#admin.site.register(Pull)
admin.site.register(Unit)
#admin.site.register(Category)
admin.site.register(Category, CategoryAdmin)
#admin.site.register(Review)

