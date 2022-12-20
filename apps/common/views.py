from django.shortcuts import render
from django.views import View

class HomeView(View):
    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, 'common/main.html', context)