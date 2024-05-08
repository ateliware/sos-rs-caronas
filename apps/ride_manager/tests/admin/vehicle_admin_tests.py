import pytest
from django.contrib.admin import AdminSite

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.admin import VehicleAdmin
from apps.ride_manager.models import Vehicle
from apps.ride_manager.tests.factories import VehicleFactory


class VehicleAdminTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.vehicle = VehicleFactory()
        self.admin = VehicleAdmin(Vehicle, AdminSite())

    def test_list_display(self):
        # Given
        expected_list_display = [
            "model",
            "color",
            "plate",
            "is_active",
        ]

        # When/Then
        self.execute_admin_tests(expected_list_display, "list_display")

    def test_search_fields(self):
        # Given
        expected_search_fields = [
            "model",
            "plate",
        ]

        # When/Then
        self.execute_admin_tests(expected_search_fields, "search_fields")

    def test_list_filter(self):
        # Given
        expected_list_filter = [
            "is_verified",
            "is_active",
        ]

        # When/Then
        self.execute_admin_tests(expected_list_filter, "list_filter")

    def test_ordering(self):
        # Given
        expected_ordering = [
            "model",
            "plate",
        ]

        # When/Then
        self.execute_admin_tests(expected_ordering, "ordering")

    def test_readonly_fields(self):
        # Given
        expected_readonly_fields = [
            "uuid",
            "person",
            "model",
            "color",
            "plate",
            "plate_picture",
            "vehicle_picture",
            "created_at",
            "updated_at",
        ]

        # When/Then
        self.execute_admin_tests(expected_readonly_fields, "readonly_fields")
