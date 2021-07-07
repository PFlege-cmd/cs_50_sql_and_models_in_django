from django.contrib import admin
from .models import Listing, Comments, Bids

# Register your models here.
admin.site.register(Listing)
admin.site.register(Comments)
admin.site.register(Bids)