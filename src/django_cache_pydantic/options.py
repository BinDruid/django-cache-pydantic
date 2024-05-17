from django.core.cache import caches
from src.django_cache_pydantic.conf import conf


class CacheMetaOptions:
    """
    Helper class for defining options for the cache meta.

    This class assists in defining options for the cache meta class used in PydanticCachedModel.
    """

    default_cache_attr = ['ttl', 'cache_backend', 'primary_key_field', 'verbose']

    def __init__(self, cls, original_cache_class) -> None:
        """
        Initialize the CacheMetaOptions instance with default or user defined values.
        """

        default_dict = {key: None for key in self.default_cache_attr}
        default_dict.update(
            {
                'ttl': conf.CACHE_PYDANTIC_DEFAULT_TTL,
                'cache_backend': caches[conf.CACHE_PYDANTIC_DEFAULT_CACHE],
                'verbose': cls.__name__,
            }
        )
        self.defaults = default_dict
        self.originals = {}
        if original_cache_class is not None:
            self.originals = original_cache_class.__dict__.copy()

    def define_options_class(self):
        """
        Dynamically defines a cache meta class with default and overridden attributes.

        returns: type: The created CacheMeta class.

        """
        original_attrs = {key: value for key, value in self.originals.items() if key in self.default_cache_attr}
        cache_meta_class_attrs = {key: original_attrs.get(key) or self.defaults[key] for key in self.default_cache_attr}
        cache_meta_class = type('CacheMeta', (), cache_meta_class_attrs)
        return cache_meta_class
