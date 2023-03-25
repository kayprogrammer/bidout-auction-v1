from django.shortcuts import render
from django.views import View
from apps.listings.models import Listing
from .models import Review


class HomeView(View):
    def get(self, request, *args, **kwargs):
        listings = Listing.objects.select_related("auctioneer")[:6]
        reviews = Review.objects.filter(show=True)[:3]
        context = {"listings": listings, "reviews": reviews}
        return render(request, "general/main.html", context)
