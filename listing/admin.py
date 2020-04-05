from django.contrib import admin
from .models import Category, Push, Pull, Review, Unit


admin.site.register(Push)
admin.site.register(Pull)
admin.site.register(Unit)
admin.site.register(Category)
admin.site.register(Review)
