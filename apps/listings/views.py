from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Listing, Category


class AllAuctionsView(View):
    def get(self, request, *args, **kwargs):
        listings = Listing.objects.select_related("auctioneer")
        categories = Category.objects.all()
        context = {"listings": listings, "categories": categories}
        return render(request, "listings/listings.html", context)

class AuctionsByCategoryView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        category = categories.filter(slug=kwargs.get('category_slug'))
        if not category:
            raise Http404("Category Not Found")
        category = category.get()
        listings = Listing.objects.filter(category=category).select_related("auctioneer", "category")
        context = {"listings": listings, "categories": categories, "category": category}
        return render(request, "listings/listings.html", context)

class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, "listings/dashboard.html", context)
