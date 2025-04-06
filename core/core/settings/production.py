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

# Override default Django logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',  # Only log errors in production
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Use SendGrid as the email backend in production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Set SendGrid SMTP server
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587  # SendGrid uses port 587 for TLS
EMAIL_USE_TLS = True  # Use TLS for secure communication
EMAIL_HOST_USER = 'apikey'  # This is the default username for SendGrid's API
EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_API_KEY')  # SendGrid API Key (from Heroku environment variable)

DEFAULT_FROM_EMAIL = '"Papers" <email@get-papers.com>'

# Shopify
SHOPIFY_WEBHOOK_SIGNATURE = os.getenv('SHOPIFY_WEBHOOK_SIGNATURE')

# FIXME: Generate and use a different secret key in production!
# SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
