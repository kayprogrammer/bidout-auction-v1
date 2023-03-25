from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, "general/main.html", context)
