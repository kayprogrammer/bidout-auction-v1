from django.shortcuts import render
from django.urls import reverse
from django.views import View

# Create your views here.

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('shop:home'))

class HomeView(View):
    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, 'shop/main.html', context)