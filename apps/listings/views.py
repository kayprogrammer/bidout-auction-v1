from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Listing


class AuctionsView(View):
    def get(self, request, *args, **kwargs):
        listings = Listing.objects.select_related("creator")
        context = {"listings": listings}
        return render(request, "listings/auctions.html", context)


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, "listings/dashboard.html", context)
