Django Cache Pydantic
=========================

Django Cache Pydantic is a minimal wrapper around django cache framework which allows you
to create pydantic instances directly inside your django project cache and retrieve them
using a similar interface to django orm.

Status
------

.. image:: https://img.shields.io/github/actions/workflow/status/bindruid/django-cache-pydantic/test.yml.svg?branch=master
   :target: https://github.com/bindruid/django-cache-pydantic/actions?workflow=Test

.. image:: https://img.shields.io/pypi/v/django-cache-pydantic.svg
   :target: https://pypi.python.org/pypi/django-cache-pydantic

.. image:: https://img.shields.io/pypi/pyversions/django-cache-pydantic.svg
   :target: https://pypi.org/project/django-cache-pydantic

.. image:: https://img.shields.io/pypi/djversions/django-cache-pydantic.svg
   :target: https://pypi.org/project/django-cache-pydantic/

Dependencies
------------

-  Pydantic >= 2.6
-  Django >= 3.2

Install
-------

.. code-block:: bash

   pip install django-cache-pydantic

Usage
-----

1. Edit settings.py and add `django_cache_pydantic` to your `INSTALLED_APPS` (also config `CACHES` setting).

2. Inherit your pydantic model from `PydanticCachedModel`.

.. code-block:: python

    from pydantic import Field, Optional
    from datetime import datetime
    from django_cache_pydantic import PydanticCachedModel


    class Person(PydanticCachedModel):
        national_id: str = Field(max_length=10, pattern=r'^\d*$')
        first_name: Optional[str] = None
        last_name: Optional[str] = None
        mobile_number: str = Field(max_length=11, pattern=r'^\d*$')
        created_at: datetime = Field(default_factory=lambda: datetime.now())

        class CacheMeta:
            ttl = 5 * 60
            primary_key_field = 'national_id'

3. Create your model instance directly into the cache via calling to `save` method or object manager `create` method.

.. code-block:: python

    # some where in your views
    person = Person(national_id='123456789', mobile_number='0930444444')
    person.save()  # will save the instance into project default cache

.. code-block:: python

    # some where in your views
    Person.objects.create(national_id='123456789', mobile_number='0930444444')  # will save the instance into project default cache

4. Retrieve your model instance from the cache via calling to object manager `get` method.

.. code-block:: python

    # some where in your views
    person = Person.objects.get(pk='123456789')
    if person is not None:
        # do some stuff

Cache pydantic meta class
---------------------------

- You can control cache pydantic models behavior using a custom meta class called `CacheMeta`.

.. code-block:: python

    class CacheMeta:
        cache_backend: str  # refers to a predefined cache settings
        ttl: int  # default timeout for instance to live in cache
        primary_key_field: str  # could be set to be used as cache key
        verbose: str  # verbose name of base model

Cache pydantic Project Settings
----------------------------------

- Default cache to save pydantic models into.

.. code-block:: python

    CACHE_PYDANTIC_DEFAULT_CACHE

- Default time to live of the pydantic cached models.

.. code-block:: python

    CACHE_PYDANTIC_DEFAULT_TTL
