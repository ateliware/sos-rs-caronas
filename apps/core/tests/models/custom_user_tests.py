import pytest
from faker import Faker

from apps.core.models import CustomUser
from apps.core.tests.base_test import BaseTest
from apps.core.tests.factories import CustomUserFactory

fake = Faker("pt_BR")


class CustomUserModelTests(BaseTest):
    def test_create_custom_user_model_instance(self):
        # Given
        expected_attrs = [
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "is_superuser",
            "password",
        ]

        # When
        user = CustomUserFactory()
        db_user = CustomUser.objects.get(pk=user.pk)

        # Then
        self.assertIsInstance(user, CustomUser)

        for attr in expected_attrs:
            with self.subTest(attr=attr):
                self.assertHasAttr(db_user, attr)
                user_attr = getattr(user, attr)
                db_user_attr = getattr(db_user, attr)
                self.assertEqual(user_attr, db_user_attr)

    def test_create_custom_user_model_instance_if_email_already_exists(self):
        # Given
        user = CustomUserFactory()
        new_user_data = CustomUserFactory.custom_user_data()
        new_user_data["email"] = user.email
        expected_error = "duplicate key value violates unique constraint"

        # When
        with pytest.raises(Exception) as error_info:
            CustomUser.objects.create(**new_user_data)

        # Then
        obtained_error = error_info.value.args[0]
        self.assertIn(expected_error, obtained_error)
