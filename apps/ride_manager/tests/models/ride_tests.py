import pytest

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.models.ride import Ride
from apps.ride_manager.tests.factories.ride_factory import RideFactory
from apps.ride_manager.tests.factories.person_factory import PersonFactory


class RideModelTests(BaseTest):

    def setUp(self):
        super().setUp()
        person = PersonFactory(user=self.user)
        self.ride_instance = RideFactory(driver=person)

    def test_create_instanse(self):
        # Given
        expected_attrs = [
            "work_shift",
            "origin",
            "destination",
            "driver",
            "vehicle",
            "notes",
            "status",
            "is_active",
        ]
        # When
        db_ride = Ride.objects.get(pk=self.ride_instance.pk)
        expected_db_ride_str = f"{self.ride_instance.origin} - {self.ride_instance.destination} - {self.ride_instance.date} - {self.ride_instance.work_shift}"

        # Then
        self.assertIsInstance(self.ride_instance, Ride)
        self.assertEqual(str(self.ride_instance), expected_db_ride_str)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(self.ride_instance, attr_name)
                ride_attr = getattr(self.ride_instance, attr_name)
                db_ride_attr = getattr(db_ride, attr_name)
                self.assertEqual(ride_attr, db_ride_attr)

    def test_ride_model_meta_verbose_names(self):
        # Given
        expected_verbose_name = "Carona"
        expected_verbose_name_plural = "Caronas"

        # When
        meta = Ride._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)

    def test_ride_create_raise_exception_when_missing_required_fields(self):
        # Given
        required_fields = [
            "date",
            "work_shift",
            "origin",
            "destination",
            "driver",
            "vehicle",
            "notes",
            "status",
            "is_active",
        ]

        for field_name in required_fields:
            with self.subTest(field=field_name):
                ride_data = RideFactory.ride_data()
                ride_data.pop(field_name)
                with pytest.raises(Exception):
                    RideFactory(**ride_data)
