from django.core.exceptions import ValidationError

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.base_test import BaseTest
from apps.ride_manager.models.voluntary import Voluntary
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.voluntary_factory import VoluntaryFactory


class VoluntaryModelTests(BaseTest):
    def test_create_voluntary_model_instance(self):
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
        voluntary = VoluntaryFactory()
        db_voluntary = Voluntary.objects.get(id=voluntary.id)

        # Then
        self.assertIsInstance(voluntary, Voluntary)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(voluntary, attr_name)
                voluntary_attr = getattr(voluntary, attr_name)
                db_voluntary_attr = getattr(db_voluntary, attr_name)
                self.assertEqual(voluntary_attr, db_voluntary_attr)

    def test_voluntary_model_verbose_names(self):
        # Given
        expected_verbose_name = "Voluntário"
        expected_verbose_name_plural = "Voluntários"

        # When
        meta = Voluntary._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)

    def test_voluntary_raise_exception_when_missing_required_fields(
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
                voluntary_data = {
                    "person": person,
                    "origin": city,
                    "date": "2021-01-01",
                }
                voluntary_data[field] = None

                with self.assertRaises(Exception):
                    Voluntary.objects.create(**voluntary_data)

    def test_voluntary_create_raise_exception_when_invalid_work_shift(
        self,
    ):
        # Given
        city = CityFactory()
        person = PersonFactory()
        voluntary_data = {
            "person": person,
            "origin": city,
            "date": "2021-01-01",
            "work_shift": "invalid_status",
        }

        # When
        with self.assertRaises(ValidationError):
            Voluntary.objects.create(**voluntary_data)

    def test_voluntary_create_raise_exception_when_invalid_status(self):
        # Given
        city = CityFactory()
        person = PersonFactory()
        voluntary_data = {
            "person": person,
            "origin": city,
            "date": "2021-01-01",
            "status": "invalid_status",
        }

        # When
        with self.assertRaises(ValidationError):
            Voluntary.objects.create(**voluntary_data)
