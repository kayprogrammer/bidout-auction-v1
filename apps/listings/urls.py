from django.urls import path
from . import views

urlpatterns = [
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
    path(
        "listings/<slug:listing_slug>/place-bid/",
        views.PlaceBidView.as_view(),
        name="place-bid",
    ),
    path(
        "create-listing/",
        views.CreateListingView.as_view(),
        name="create-listing",
    ),
    path(
        "listings/<slug:listing_slug>/status/update/",
        views.UpdateListingStatus.as_view(),
        name="listing-status-update",
    ),
    # Dashboard Urls
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path(
        "dashboard/listings/",
        views.AuctioneerListingsView.as_view(),
        name="auctioneer-listings",
    ),
    path(
        "dashboard/listings/<slug:listing_slug>/bids/",
        views.AuctioneerListingBidsView.as_view(),
        name="auctioneer-listing-bids",
    ),
    path(
        "dashboard/listings/<slug:listing_slug>/update/",
        views.UpdateListingView.as_view(),
        name="update-listing",
    ),
]
