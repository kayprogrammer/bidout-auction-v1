"""
WSGI config for bidout project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""
import os, sys
if os.environ.get('SETTINGS') == 'production':
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from decouple import config

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"bidout.settings.{config('SETTINGS')}")

application = get_wsgi_application()
app = application