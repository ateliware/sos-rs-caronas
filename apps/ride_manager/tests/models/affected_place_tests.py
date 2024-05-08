import pytest

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.models.affected_place import AffectedPlace
from apps.ride_manager.tests.factories.affected_place_factory import (
    AffectedPlaceFactory,
)


class AffectedPlaceModelTests(BaseTest):
    def test_create_affected_place_model_instance(self):
        # Given
        expected_attrs = [
            "city",
            "main_person",
            "main_contact",
            "address",
            "informations",
        ]

        # When
        affected_place = AffectedPlaceFactory()
        db_affected_place = AffectedPlace.objects.get(pk=affected_place.pk)
        expected_db_affected_place_str = f"{db_affected_place.description}"

        # Then
        self.assertIsInstance(affected_place, AffectedPlace)
        self.assertEqual(str(affected_place), expected_db_affected_place_str)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(affected_place, attr_name)
                affected_place_attr = getattr(affected_place, attr_name)
                db_affected_place_attr = getattr(db_affected_place, attr_name)
                self.assertEqual(affected_place_attr, db_affected_place_attr)

    def test_affected_place_model_meta_verbose_names(self):
        # Given
        expected_verbose_name = "Local Afetado"
        expected_verbose_name_plural = "Locais Afetados"

        # When
        meta = AffectedPlace._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)

    def test_affected_place_create_raise_exception_when_missing_required_fields(
        self,
    ):
        # Given
        test_cases = ["city", "main_person", "main_contact"]

        for attr_name in test_cases:
            # When
            with self.subTest(attr=attr_name):
                test_data = AffectedPlaceFactory.affected_place_data()
                test_data[attr_name] = None

                # Then
                with self.assertRaises(Exception):
                    AffectedPlace.objects.create(**test_data)
