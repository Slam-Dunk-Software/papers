from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS : list[str | None] = []

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES: dict[str, dict[str, str | None]] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'papers_development',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
