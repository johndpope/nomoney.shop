from django.contrib import admin
from .models import Bid, BidPosition

class BookAdmin(admin.ModelAdmin):
     model= Bid
     filter_horizontal = ('positions',) #If you don't specify this, you will get a multiple select widget.

admin.site.register(BidPosition)
admin.site.register(Bid, BookAdmin)
