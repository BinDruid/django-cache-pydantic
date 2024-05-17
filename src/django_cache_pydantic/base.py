from typing import ClassVar
from uuid import uuid4

from pydantic import BaseModel, computed_field

from .manager import CacheManager
from .options import CacheMetaOptions


class PydanticCachedModel(BaseModel):
    """
    A Pydantic model with caching functionality.

    This class extends Pydantic's BaseModel and provides caching features.

    Attributes:
        objects (ClassVar): Model manager with a similar interface to django ORM.
    """

    objects: ClassVar = CacheManager()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs) -> None:
        """
        Initialize the PydanticCachedModel subclass.
        Add CacheMeta class to subclassed children.

        raises: TypeError: If CacheMeta is not a class.

        """
        super().__pydantic_init_subclass__(**kwargs)
        cache_class = getattr(cls, 'CacheMeta', None)
        if cache_class is not None and type(cache_class) is not type:
            raise TypeError('CacheMeta should be a class and not of type %s' % type(cache_class))
        new_cache_class = CacheMetaOptions(cls, cache_class).define_options_class()
        setattr(cls, '_cache_meta', new_cache_class)

    def __init__(self, /, **data):
        super().__init__(**data)
        _internal_id = uuid4().hex
        setattr(self, '_internal_id', _internal_id)

    @computed_field
    def id(self) -> str:
        """
        Computed property for generating the composite ID.

        :return: str: The composite ID.
        """
        pk_field = getattr(self.CacheMeta, 'primary_key_field', None)
        return getattr(self, pk_field) if pk_field is not None else self._internal_id

    def _get_composite_id(self) -> str:
        """
        Returns composite ID composed of class name and internal id.
        :return: str: The composite ID.
        """
        return f'{self.__class__.__name__.lower()}__{self.id}'

    @computed_field
    def pk(self) -> str:
        return self.id

    def save(self):
        """
        Saves the instance in the cache with a specified time-to-live (ttl).
        """
        cache = self._cache_meta.cache_backend
        composite_id = self._get_composite_id()
        cache.set(composite_id, self, self._cache_meta.ttl)

    def delete(self):
        """
        Delete the instance from the cache.
        """
        cache = self._cache_meta.cache_backend
        composite_id = self._get_composite_id()
        cache.delete(composite_id)
