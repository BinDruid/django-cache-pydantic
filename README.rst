Django Cache Pydantic
=========================

Django cache pydantic is a minimal wrapper around django cache framework which allows you
to create pydantic instances directly inside your django project cache and retrieve them
using a similar interface like django orm.

Status
------

.. image:: https://github.com/bindruid/django-cache-pydantic/workflows/Test/badge.svg?branch=master
   :target: https://github.com/bindruid/django-cache-pydantic/actions

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

.. code:: bash

   pip install django-cache-pydantic

Usage
-----

1. Edit settings.py and add `django_cache_pydantic` to your INSTALLED_APPS (also config CACHES setting)


2. Inherit your pydantic model from `PydanticCachedModel`

.. code:: python

    from from django_cache_pydantic import PydanticCachedModel


    class Person(PydanticCachedModel):
        national_id: str = Field(max_length=10, pattern=r'^\d*$')
        first_name: Optional[Annotated[str, Field(max_length=20)]] = None
        last_name: Optional[Annotated[str, Field(max_length=20)]] = None
        mobile_number: str = Field(max_length=11, pattern=r'^\d*$')
        created_at: Annotated[datetime.datetime, Field(default_factory=lambda: datetime.datetime.now())]

        class CacheMeta:
            ttl = 5 * 60
            primary_key_field = 'national_id'


3. Create your model instance directly into the cache via calling to `save` method or object manager `create` method

.. code:: python

    # some where in your views
    person = Person(national_id='123456789', mobile_number='0930444444')
    person.save() # will save the instance into project default cache

.. code:: python

    # some where in your views
    Person.objects.create(national_id='123456789', mobile_number='0930444444') # will save the instance into project default cache


4. Retrieve your model instance from the cache via calling to object manager `get` method

.. code:: python

    # some where in your views
    person = Person.objects.get(pk='123456789')
    if person is not None:
        # do some stuff


Cache pydantic Settings
-----------------
- Default cache to save pydantic models into

.. code:: python

    CACHE_PYDANTIC_DEFAULT_CACHE

- Default time to live of the pydantic cached models

.. code:: python

    CACHE_PYDANTIC_DEFAULT_TTL
