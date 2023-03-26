from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("suscribe/", views.SuscriberView.as_view(), name="suscribe"),
]
