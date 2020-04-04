from django.contrib import admin
from .models import Category, Listing, Review, Type, Unit

admin.site.register(Listing)
admin.site.register(Unit)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Type)

