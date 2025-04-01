from .base import *  # noqa: F403
import os

DEBUG = False
ALLOWED_HOSTS: list[str | None] = [os.getenv("HOST_NAME")]

# Production database (Heroku)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}
