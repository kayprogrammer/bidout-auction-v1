from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("listings/", views.AuctionsView.as_view(), name="listings"),
]
