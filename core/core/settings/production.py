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

# Use SendGrid as the email backend in production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Set SendGrid SMTP server
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587  # SendGrid uses port 587 for TLS
EMAIL_USE_TLS = True  # Use TLS for secure communication
EMAIL_HOST_USER = 'apikey'  # This is the default username for SendGrid's API
EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_API_KEY')  # SendGrid API Key (from Heroku environment variable)

DEFAULT_FROM_EMAIL = '"Papers" <email@slamdunk.software>'

