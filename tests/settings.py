from __future__ import annotations

SECRET_KEY = 'NOTASECRET'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = ['django_cache_pydantic']

USE_TZ = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
