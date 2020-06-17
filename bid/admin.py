from django.contrib import admin
from .models import Bid, BidPush, BidPull


class BidPushAdmin(admin.TabularInline):
    model = BidPush


class BidPullAdmin(admin.TabularInline):
    model = BidPull


class BidAdmin(admin.ModelAdmin):
    inlines = [BidPushAdmin, BidPullAdmin, ]


admin.site.register(Bid, BidAdmin)
