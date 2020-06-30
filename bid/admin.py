from django.contrib import admin
from .models import Bid, BidPosition


class BidPositionAdmin(admin.TabularInline):
    model = BidPosition


class BidAdmin(admin.ModelAdmin):
    inlines = [BidPositionAdmin, ]


admin.site.register(Bid, BidAdmin)
