from apps.ride_manager.admin.phone_validation_admin import (
    PhoneValidationAdmin,
)
from apps.ride_manager.models.phone_validation import PhoneValidation
from apps.ride_manager.tests.factories.phone_validation_factory import (
    PhoneValidationFactory,
)
from apps.core.tests.base_test import BaseTest


class RecoveryPasswordValidatorAdminTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.phone_validation = PhoneValidationFactory()
        self.admin = PhoneValidationAdmin(
            model=PhoneValidation,
            admin_site=None,
        )

    def test_list_display(self):
        # Given
        expected_list_display = [
            "uuid",
            "phone",
            "is_active",
        ]

        # When
        result = self.admin.list_display

        # Then
        for item in expected_list_display:
            with self.subTest(item=item):
                self.assertIn(item, result)

    def test_fields(self):
        # Given
        expected_fields = [
            "uuid",
            "integration_sid",
            "phone",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When/Then
        self.execute_admin_tests(expected_fields, "fields")

    def test_readonly_fields(self):
        # Given
        expected_readonly_fields = [
            "uuid",
            "integration_sid",
            "phone",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When/Then
        self.execute_admin_tests(expected_readonly_fields, "readonly_fields")

    def test_ordering(self):
        # Given
        expected_ordering = [
            "-created_at",
        ]

        # When/Then
        self.execute_admin_tests(expected_ordering, "ordering")