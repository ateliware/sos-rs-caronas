from django.core.exceptions import ValidationError

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.base_test import BaseTest
from apps.ride_manager.models.work_availability import WorkAvailability
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.work_availability_factory import (
    WorkAvailabilityFactory,
)


class WorkAvailabilityModelTests(BaseTest):
    def test_create_work_availability_model_instance(self):
        # Given
        expected_attrs = [
            "id",
            "person",
            "origin",
            "destination",
            "any_destination",
            "date",
            "work_shift",
            "status",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When
        work_availability = WorkAvailabilityFactory()
        db_work_availability = WorkAvailability.objects.get(
            id=work_availability.id
        )

        # Then
        self.assertIsInstance(work_availability, WorkAvailability)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(work_availability, attr_name)
                work_availability_attr = getattr(work_availability, attr_name)
                db_work_availability_attr = getattr(
                    db_work_availability, attr_name
                )
                self.assertEqual(
                    work_availability_attr, db_work_availability_attr
                )

    def test_work_availability_model_verbose_names(self):
        # Given
        expected_verbose_name = "Disponibilidade de trabalho"
        expected_verbose_name_plural = "Disponibilidades de trabalho"

        # When
        meta = WorkAvailability._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)

    def test_work_availability_raise_exception_when_missing_required_fields(
        self,
    ):
        # Given
        test_cases = [
            "person",
            "origin",
            "date",
        ]
        city = CityFactory()
        person = PersonFactory()

        for field in test_cases:
            # When
            with self.subTest(field=field):
                work_availability_data = {
                    "person": person,
                    "origin": city,
                    "date": "2021-01-01",
                }
                work_availability_data[field] = None

                with self.assertRaises(Exception):
                    WorkAvailability.objects.create(**work_availability_data)

    def test_work_availability_create_raise_exception_when_invalid_work_shift(
        self,
    ):
        # Given
        city = CityFactory()
        person = PersonFactory()
        work_availability_data = {
            "person": person,
            "origin": city,
            "date": "2021-01-01",
            "work_shift": "invalid_status",
        }

        # When
        with self.assertRaises(ValidationError):
            WorkAvailability.objects.create(**work_availability_data)

    def test_work_availability_create_raise_exception_when_invalid_status(self):
        # Given
        city = CityFactory()
        person = PersonFactory()
        work_availability_data = {
            "person": person,
            "origin": city,
            "date": "2021-01-01",
            "status": "invalid_status",
        }

        # When
        with self.assertRaises(ValidationError):
            WorkAvailability.objects.create(**work_availability_data)
