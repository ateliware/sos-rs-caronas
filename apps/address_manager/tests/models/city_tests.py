import pytest

from apps.address_manager.models import City
from apps.address_manager.tests.factories import CityFactory
from apps.core.tests.base_test import BaseTest


class CityModelTests(BaseTest):
    def test_create_city_model_instance(self):
        # Given
        expected_attrs = ["name", "state"]

        # When
        city = CityFactory()
        db_city = City.objects.get(pk=city.pk)
        expected_db_city_str = f"{db_city.name} | {db_city.state.code}"

        # Then
        self.assertIsInstance(city, City)
        self.assertEqual(str(city), expected_db_city_str)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(city, attr_name)
                city_attr = getattr(city, attr_name)
                db_city_attr = getattr(db_city, attr_name)
                self.assertEqual(city_attr, db_city_attr)

    def test_city_model_meta_verbose_names(self):
        # Given
        expected_verbose_name = "Cidade"
        expected_verbose_name_plural = "Cidades"

        # When
        meta = City._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)

    def test_city_create_raise_exception_when_missing_required_fields(self):
        # Given
        test_cases = ["name", "state"]

        for attr_name in test_cases:
            # When
            with self.subTest(attr=attr_name):
                test_data = CityFactory.city_data()
                test_data[attr_name] = None

                # Then
                with self.assertRaises(Exception):
                    City.objects.create(**test_data)
