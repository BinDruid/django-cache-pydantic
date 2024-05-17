from __future__ import annotations

from django.conf import settings
from src.django_cache_pydantic.defaults import default_cache, default_ttl


class DjangoSettings:
    @property
    def CACHE_PYDANTIC_DEFAULT_CACHE(self) -> str:
        return getattr(settings, 'CACHE_PYDANTIC_DEFAULT_CACHE', default_cache)

    @property
    def CACHE_PYDANTIC_DEFAULT_TTL(self) -> int:
        return getattr(settings, 'CACHE_PYDANTIC_DEFAULT_TTL', default_ttl)


conf = DjangoSettings()
