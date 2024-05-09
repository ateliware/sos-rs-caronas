import pytest

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.models import Vehicle
from apps.ride_manager.tests.factories.vehicle_factory import VehicleFactory


class VehicleModelTests(BaseTest):
    def test_create_vehicle_model_instance(self):
        # Given
        expected_attrs = [
            "model",
            "person",
            "color",
            "plate",
            "plate_picture",
            "vehicle_picture",
            "is_verified",
        ]

        # When
        vehicle = VehicleFactory()
        db_vehicle = Vehicle.objects.get(pk=vehicle.pk)

        # Then
        self.assertIsInstance(vehicle, Vehicle)
        self.assertEqual(str(vehicle), vehicle.model)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertTrue(hasattr(vehicle, attr_name))
                vehicle_attr = getattr(vehicle, attr_name)
                db_vehicle_attr = getattr(db_vehicle, attr_name)
                self.assertEqual(vehicle_attr, db_vehicle_attr)

    def test_vehicle_model_meta_verbose_names(self):
        # Given
        expected_verbose_name = "Veículo"
        expected_verbose_name_plural = "Veiculos"

        # When
        meta = Vehicle._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)

    def test_vehicle_create_raise_exception_when_missing_required_fields(self):
        # Given
        required_fields = [
            "model",
            "person",
            "color",
            "plate",
            "plate_picture",
            "vehicle_picture",
            "is_verified",
        ]

        for field_name in required_fields:
            # When
            with self.subTest(attr=field_name):
                test_data = VehicleFactory.build()
                setattr(test_data, field_name, None)

                # Then
                with self.assertRaises(Exception):
                    test_data.save()
