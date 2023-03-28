from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("listings/", views.AllAuctionsView.as_view(), name="listings"),
    path(
        "listings/<slug:listing_slug>/",
        views.AuctionDetailView.as_view(),
        name="listing-detail",
    ),
    path(
        "categories/<slug:category_slug>/",
        views.AuctionsByCategoryView.as_view(),
        name="category-listings",
    ),
    path("watch-list/", views.WatchListView.as_view(), name="watch-list"),
    path("listings/<slug:listing_slug>/place-bid/", views.PlaceBidView.as_view(), name="place-bid"),
]
