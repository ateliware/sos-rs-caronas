from apps.ride_manager.models import PhoneValidation
from apps.ride_manager.tests.factories.phone_validation_factory import (
    PhoneValidationFactory,
)
from apps.core.tests.base_test import BaseTest


class PhoneValidationTests(BaseTest):
    def test_create_phone_validation_model_instance(self):
        # Given
        expected_attrs = [
            "integration_sid",
            "phone",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When
        phone_validation = PhoneValidationFactory()
        db_phone_validation = PhoneValidation.objects.get(
            uuid=phone_validation.uuid
        )

        # Then
        self.assertIsInstance(phone_validation, PhoneValidation)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(db_phone_validation, attr_name)
                factory_attr = getattr(phone_validation, attr_name)
                db_attr = getattr(db_phone_validation, attr_name)
                self.assertEqual(factory_attr, db_attr)

    def test_phone_validation_meta_verbose_names(self):
        # Given
        expected_verbose_name = "Validação de telefone"
        expected_verbose_name_plural = "Validações de telefone"

        # When
        meta = PhoneValidation._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)
