from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from apps.listings.models import Listing
from .models import Review, Subscriber


class HomeView(View):
    def get(self, request, *args, **kwargs):
        listings = Listing.objects.select_related("auctioneer")[:6]
        reviews = Review.objects.filter(show=True)[:3]
        context = {"listings": listings, "reviews": reviews}
        return render(request, "general/main.html", context)


class SubscriberView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        Subscriber.objects.get_or_create(email=email)
        messages.success(request, "Subscribed successfully")
        redirect_url = request.META.get("HTTP_REFERER") or "/"
        return redirect(redirect_url)
