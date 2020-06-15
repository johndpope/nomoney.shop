from django.contrib import admin
from .models import Bid, BidPosition

class BidPositionAdmin(admin.ModelAdmin):
    model= BidPosition
    #filter_horizontal = ('positions',) #If you don't specify this, you will get a multiple select widget.

admin.site.register(BidPosition)
admin.site.register(Bid, BidPositionAdmin)
