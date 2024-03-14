class Manager:
    """
    Manager class for handling model instances and cache interactions.

    This class provides methods for creating and retrieving pydantic model instances.
    """

    def __init__(self, model_class, cache_meta_class) -> None:
        self.model_class = model_class
        self.cache_meta_class = cache_meta_class

    def create(self, **kwargs):
        """
        Create a new model instance, save it to the cache, and return the instance.
        """

        instance = self.model_class(**kwargs)
        instance.save()
        return instance

    def get(self, pk):
        """
        Retrieve a model instance from the cache based on the primary key.
        """

        cache = self.cache_meta_class.cache_backend
        return cache.get(pk)


class CacheManager:
    """
    Descriptor class allowing to access objects manager from class not instances.
    """

    manager_class = Manager

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, cls):
        """
        Create a manager for owner class and add it to cache meta class of the owner.
        raises: AttributeError if trying to access the manager from an instance.
        """

        if obj is not None:
            raise AttributeError("Manager for %s isn't accessible via %s instances" % (self.name, cls.__name__))
        cache_manager = getattr(cls._cache_meta, 'manager', None)
        if cache_manager is None:
            cache_manager = self.manager_class(cls, cls._cache_meta)
            setattr(cls._cache_meta, 'manager', cache_manager)
        return cache_manager
