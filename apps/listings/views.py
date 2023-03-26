from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Listing, Category


class AuctionsView(View):
    def get(self, request, *args, **kwargs):
        listings = Listing.objects.select_related("auctioneer")
        categories = Category.objects.all()
        context = {"listings": listings, "categories": categories}
        return render(request, "listings/listings.html", context)


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, "listings/dashboard.html", context)
