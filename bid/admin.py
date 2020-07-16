""" Admin settings for the bid module """
from django.contrib import admin
from .models import Bid, BidPosition


class BidPositionAdmin(admin.TabularInline):
    """ tabular inline for bid position """
    model = BidPosition


class BidAdmin(admin.ModelAdmin):
    """ admin class for bid admin with bidposition inline """
    inlines = [BidPositionAdmin, ]


admin.site.register(Bid, BidAdmin)
