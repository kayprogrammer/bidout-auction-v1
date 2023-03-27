from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Listing, Category, WatchList, Bid
import json


class AllAuctionsView(View):
    def get(self, request, *args, **kwargs):
        listings = Listing.objects.select_related("auctioneer")
        categories = Category.objects.all()
        context = {"listings": listings, "categories": categories}
        return render(request, "listings/listings.html", context)


class AuctionDetailView(View):
    def get(self, request, *args, **kwargs):
        listings = Listing.objects.all()
        listing = listings.filter(slug=kwargs.get("listing_slug"))
        if not listing.exists():
            raise Http404("Listing Not Found!")
        listing = listing.get()

        related_listings = (
            listings.filter(category=listing.category)
            .exclude(id=listing.id)
            .select_related("auctioneer")[:3]
        )

        latest_bids = Bid.objects.filter(listing=listing).select_related('user', 'listing')[:3]

        context = {"listing": listing, "related_listings": related_listings, "latest_bids": latest_bids}
        return render(request, "listings/listing-detail.html", context)


class AuctionsByCategoryView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        category = categories.filter(slug=kwargs.get("category_slug"))
        if not category:
            raise Http404("Category Not Found")
        category = category.get()
        listings = Listing.objects.filter(category=category).select_related(
            "auctioneer", "category"
        )
        context = {
            "listings": listings,
            "categories": categories,
            "category": category,
        }
        return render(request, "listings/listings.html", context)


class WatchListView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        listings = WatchList.objects.filter(
            Q(user_id=user.pk, session_key=None) | Q(user=None, session_key=user)
        ).select_related("user", "listing")
        context = {"listings": listings}
        return render(request, "listings/watchlist.html", context)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = request.user
        listing = get_object_or_404(Listing, slug=data.get("listing_slug"))
        if user.is_authenticated:
            WatchList.objects.get_or_create(user=user, listing=listing)
        else:
            WatchList.objects.get_or_create(session_key=user, listing=listing)

        return JsonResponse({"success": True})

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = request.user
        listing_slug = data.get("listing_slug")
        watch_list = WatchList.objects.filter(
            Q(user_id=user.pk, session_key=None) | Q(user=None, session_key=user)
        ).filter(listing__slug=listing_slug)
        watch_list.delete()
        return JsonResponse({"success": True})


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, "listings/dashboard.html", context)
