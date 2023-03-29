from django.utils import timezone
from django.contrib.auth.models import AnonymousUser


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        try:
            tzname = "UTC"
            localtz = request.COOKIES.get("localtz")
            if user.tz:
                tzname = user.tz.name
            elif localtz:
                tzname = localtz
            timezone.activate(tzname)
        except:
            timezone.deactivate()

        response = self.get_response(request)
        return response


class CustomAnonymousUser(AnonymousUser):
    def __init__(self, request):
        self.request = request

    def __str__(self):
        request = self.request
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        return session_key


class CustomUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            request.user = CustomAnonymousUser(request)
        response = self.get_response(request)
        return response
