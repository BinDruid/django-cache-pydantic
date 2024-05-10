from __future__ import annotations

import datetime
from typing import Annotated, Optional

import time_machine
from django.core.cache import caches
from django.test import SimpleTestCase
from pydantic import Field

from src.django_cache_pydantic import PydanticCachedModel

default_cache = caches['default']
default_ttl = 60 * 10


class SampleTestModel(PydanticCachedModel):
    username: Optional[Annotated[str, Field(max_length=6)]] = None
    mobile_number: str = Field(max_length=11, pattern=r'^\d*$')
    created_at: Annotated[datetime.datetime, Field(default_factory=lambda: datetime.datetime.now())]

    class CacheMeta:
        ttl = default_ttl
        primary_key_field = 'username'


class TestCachedPydanticModel(SimpleTestCase):

    def tearDown(self):
        default_cache.clear()

    def test_create_new_cache_instance_via_object_manager(self):
        creation_context = {'username': 'ali', 'mobile_number': '09304444444'}
        new_instance = SampleTestModel.objects.create(**creation_context)
        cache_id = new_instance._get_composite_id()
        cache_instance = default_cache.get(cache_id)
        value_under_test = new_instance.pk
        value_expected = cache_instance.pk
        self.assertEqual(value_under_test, value_expected, msg='Did not create into cache')

    def test_create_new_cache_instance_via_save_method(self):
        creation_context = {'username': 'ali', 'mobile_number': '09304444444'}
        new_instance = SampleTestModel(**creation_context)
        new_instance.save()
        cache_id = new_instance._get_composite_id()
        cache_instance = default_cache.get(cache_id)
        value_under_test = new_instance.pk
        value_expected = cache_instance.pk
        self.assertEqual(value_under_test, value_expected, msg='Did not create into cache')

    def test_retrieve_cache_instance_via_get_method(self):
        creation_context = {'username': 'ali', 'mobile_number': '09304444444'}
        new_instance = SampleTestModel.objects.create(**creation_context)
        cache_instance = SampleTestModel.objects.get(new_instance.pk)
        value_under_test = new_instance.pk
        value_expected = cache_instance.pk
        self.assertEqual(value_under_test, value_expected, msg='Did not get expected from cache')

    def test_retrieve_cache_instance_via_get_method_and_user_defined_pk(self):
        creation_context = {'username': 'ali', 'mobile_number': '09304444444'}
        new_instance = SampleTestModel.objects.create(**creation_context)
        cache_instance = SampleTestModel.objects.get(creation_context['username'])
        value_under_test = new_instance.pk
        value_expected = cache_instance.pk
        self.assertEqual(value_under_test, value_expected, msg='Did not get expected from cache')

    def test_cache_instance_still_in_cache_before_ttl(self):
        creation_context = {'username': 'ali', 'mobile_number': '09304444444'}
        new_instance = SampleTestModel.objects.create(**creation_context)
        with time_machine.travel(new_instance.created_at, tick=False) as time_traveller:
            time_shift = datetime.timedelta(seconds=default_ttl - 20)
            time_traveller.shift(time_shift)
            cache_id = new_instance._get_composite_id()
            cache_instance = default_cache.get(cache_id)
            value_under_test = new_instance.pk
            value_expected = cache_instance.pk
            self.assertEqual(value_under_test, value_expected, msg='Did not get expected from cache')
