from __future__ import annotations

from src.cache_pydantic.defaults import default_cache
from src.cache_pydantic.defaults import default_ttl
from django.conf import settings


class DjangoSettings:

    @property
    def CACHE_PYDANTIC_DEFAULT_CACHE(self) -> str:
        return getattr(settings, "CACHE_PYDANTIC_DEFAULT_CACHE", default_cache)

    @property
    def CACHE_PYDANTIC_DEFAULT_TTL(self) -> int:
        return getattr(settings, "CACHE_PYDANTIC_DEFAULT_TTL", default_ttl)


conf = DjangoSettings()
