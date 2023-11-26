from .base import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": config("POSTGRES_ENGINE"),
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("PG_HOST"),
        "PORT": config("PG_PORT"),
    }
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True