from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "morning_info",
        "USER": "admin",
        "PASSWORD": get_secret("DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": "5432",
    }
}
