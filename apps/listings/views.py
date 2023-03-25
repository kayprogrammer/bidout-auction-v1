from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Listing
from apps.general.models import Review


class HomeView(View):
    def get(self, request, *args, **kwargs):
        listings = Listing.objects.select_related("creator")[:6]
        reviews = Review.objects.filter(show=True)[:3]
        context = {"listings": listings, "reviews": reviews}
        return render(request, "listings/dashboard.html", context)


class AuctionsView(View):
    def get(self, request, *args, **kwargs):
        listings = Listing.objects.select_related("creator")
        context = {"listings": listings}
        return render(request, "listings/auctions.html", context)


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, "listings/dashboard.html", context)
