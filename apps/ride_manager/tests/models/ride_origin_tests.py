import pytest

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.base_test import BaseTest
from apps.ride_manager.models.ride_origin import RideOrigin
from apps.ride_manager.tests.factories.ride_origin_factory import (
    RideOriginFactory,
)


class RideOriginModelTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.city = CityFactory()

    def test_create_ride_origin_model_instance(self):
        # Given
        expected_attrs = ["city", "enabled"]

        # When
        ride_origin = RideOrigin.objects.create(city=self.city)
        db_ride_origin = RideOrigin.objects.get(pk=ride_origin.pk)
        expected_db_ride_origin_str = f"{db_ride_origin.city.name}"

        # Then
        self.assertIsInstance(ride_origin, RideOrigin)
        self.assertEqual(str(ride_origin), expected_db_ride_origin_str)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(ride_origin, attr_name)
                ride_origin_attr = getattr(ride_origin, attr_name)
                db_ride_origin_attr = getattr(db_ride_origin, attr_name)
                self.assertEqual(ride_origin_attr, db_ride_origin_attr)

    def test_ride_origin_model_meta_verbose_names(self):
        # Given
        expected_verbose_name = "Origem da Carona"
        expected_verbose_name_plural = "Origens das Caronas"

        # When
        meta = RideOrigin._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)

    def test_ride_origin_create_raise_exception_when_missing_required_fields(
        self,
    ):
        # Given
        test_cases = ["city"]

        for attr_name in test_cases:
            # When
            with self.subTest(attr=attr_name):
                test_data = RideOriginFactory.ride_origin_data()
                test_data[attr_name] = None

                # Then
                with pytest.raises(Exception):
                    test_data.save()
