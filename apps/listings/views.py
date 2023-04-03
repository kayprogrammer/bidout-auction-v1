from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse

from apps.accounts.mixins import LoginRequiredMixin
from .models import Listing, Category, WatchList, Bid
from .forms import CreateListingForm, UpdateProfileForm

from decimal import Decimal
import json


class AllAuctionsView(View):
    def get(self, request):
        listings = Listing.objects.select_related("auctioneer")
        categories = Category.objects.all()
        context = {"listings": listings, "categories": categories}
        return render(request, "listings/general/listings.html", context)


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

        latest_bids = Bid.objects.filter(listing=listing).select_related(
            "user", "listing"
        )[:3]

        context = {
            "listing": listing,
            "related_listings": related_listings,
            "latest_bids": latest_bids,
        }
        return render(request, "listings/general/listing-detail.html", context)


class AuctionsByCategoryView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        category_slug = kwargs.get("category_slug")
        category = categories.filter(slug=category_slug)
        if not category.exists():
            if not category_slug == "other":
                raise Http404("Category Not Found")
            category = None
        else:
            category = category.get()

        listings = Listing.objects.filter(category=category).select_related(
            "auctioneer", "category"
        )
        context = {
            "listings": listings,
            "categories": categories,
            "category": category,
        }
        return render(request, "listings/general/listings.html", context)


class WatchListView(View):
    def get(self, request):
        user = request.user
        listings = WatchList.objects.filter(
            Q(user_id=user.pk, session_key=None) | Q(user=None, session_key=user)
        ).select_related("user", "listing")
        context = {"listings": listings}
        return render(request, "listings/general/watchlist.html", context)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = request.user
        listing = get_object_or_404(Listing, slug=data.get("listing_slug"))
        if user.is_authenticated:
            WatchList.objects.get_or_create(user=user, listing=listing)
        else:
            WatchList.objects.get_or_create(session_key=user, listing=listing)

        return JsonResponse({"success": True})

    def delete(self, request):
        data = json.loads(request.body)
        user = request.user
        listing_slug = data.get("listing_slug")
        user_watch_list = WatchList.objects.filter(
            Q(user_id=user.pk, session_key=None) | Q(user=None, session_key=user)
        )

        left = user_watch_list.count()
        watch_list = user_watch_list.filter(listing__slug=listing_slug)
        watch_list.delete()
        return JsonResponse({"success": True, "left": left - 1})


class PlaceBidView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        listing = get_object_or_404(Listing, slug=kwargs.get("listing_slug"))
        amount = request.POST.get("amount")
        page = request.POST.get("page")
        response = {"status": "error"}

        if amount:
            amount = Decimal(amount)
            if listing.auctioneer == user:
                response["message"] = "You can't bid your product!"
            elif not listing.active:
                response["message"] = "This auction is closed!"
            elif listing.time_left_seconds < 1:
                response["message"] = "This auction is expired and closed!"
            elif amount < listing.price:
                response[
                    "message"
                ] = "Bid amount cannot be less than the bidding price!"
            elif amount <= listing.get_highest_bid:
                response["message"] = "Bid amount must be more than the highest bid!"
            else:
                bid, created = Bid.objects.get_or_create(
                    user=request.user, listing=listing
                )
                bid.amount = amount
                bid.save()
                response["status"] = "success"
                amount = round(bid.amount, 2)
                response["amount"] = f"{amount:,}"
                response["page"] = page

        return JsonResponse(response)


class CreateListingView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateListingForm()
        categories = Category.objects.all()
        context = {"form": form, "categories": categories}
        return render(request, "listings/dashboard/create-listing.html", context)

    def post(self, request):
        categories = Category.objects.all()
        form = CreateListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.auctioneer = request.user
            listing.save()
            messages.success(request, "Listing created successfully")
            return redirect("/")
        context = {"form": form, "categories": categories}
        return render(request, "listings/create-listing.html", context)


# ################
# DASHBOARD VIEWS
# ################
class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {}
        page = request.GET.get("page")
        if page and page == "profile":
            form = UpdateProfileForm(instance=user)
            context["form"] = form
            context["profile"] = True
        else:
            listings = Listing.objects.filter(auctioneer=user).select_related(
                "auctioneer", "category"
            )[:10]
            context["listings"] = listings
        return render(request, "listings/dashboard/main.html", context)

    def post(self, request):
        user = request.user
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
        return redirect("/dashboard/?page=profile")


class AuctioneerListingsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        listings = Listing.objects.filter(auctioneer=user).select_related(
            "auctioneer", "category"
        )
        context = {"listings": listings}
        return render(request, "listings/dashboard/all-listings.html", context)


class AuctioneerListingBidsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        listing = get_object_or_404(
            Listing, auctioneer=user, slug=kwargs.get("listing_slug")
        )
        bids = listing.bids.all()
        context = {"listing": listing, "bids": bids}
        return render(request, "listings/dashboard/bids.html", context)


class UpdateListingStatus(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        listing = get_object_or_404(
            Listing, auctioneer=request.user, slug=kwargs.get("listing_slug")
        )
        if listing.active and listing.time_left_seconds > 0:
            listing.active = False
        else:
            if listing.closing_date < timezone.now():
                messages.error(request, "Auction already expired!")
                return redirect(request.META.get("HTTP_REFERER"))
            listing.active = True
        listing.save()
        return redirect(request.META.get("HTTP_REFERER"))


class UpdateListingView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        listing = get_object_or_404(
            Listing, auctioneer=user, slug=kwargs.get("listing_slug")
        )
        form = CreateListingForm(
            instance=listing, initial={"category": listing.category or "Other"}
        )
        categories = Category.objects.all()
        context = {"listing": listing, "form": form, "categories": categories}
        return render(request, "listings/dashboard/create-listing.html", context)

    def post(self, request, *args, **kwargs):
        # Could have used a put method but html form only accepts get or post
        user = request.user
        categories = Category.objects.all()
        listing = get_object_or_404(
            Listing, auctioneer=user, slug=kwargs.get("listing_slug")
        )
        form = CreateListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing updated successfully")
            return redirect(
                reverse("update-listing", kwargs={"listing_slug": listing.slug})
            )
        context = {"form": form, "categories": categories}
        return render(request, "listings/dashboard/create-listing.html", context)
