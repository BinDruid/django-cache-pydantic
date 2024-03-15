from __future__ import annotations

SECRET_KEY = 'NOTASECRET'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = ['cache_pydantic']

USE_TZ = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
