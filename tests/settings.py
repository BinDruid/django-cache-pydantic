from __future__ import annotations

SECRET_KEY = 'NOTASECRET'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = ['cache_pydantic']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
