from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    list_filter = ["name"]


class ListingAdmin(admin.ModelAdmin):
    list_display = ["auctioneer", "name", "slug", "price", "closing_date", "active"]
    list_filter = ["auctioneer", "name", "price", "closing_date", "active"]


class BidAdmin(admin.ModelAdmin):
    list_display = ["user", "listing", "amount"]
    list_filter = ["amount"]


class WatchListAdmin(admin.ModelAdmin):
    list_display = ["user", "listing", "session_key"]
    list_filter = ["user", "listing", "session_key"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(WatchList, WatchListAdmin)
