from django import forms
from django.test import TestCase
from faker import Faker

from apps.core.forms.custom_user_forms import CustomUserCreationForm
from apps.core.utils.regex_utils import get_only_numbers

fake = Faker("pt_BR")


class CustomUserFormsTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake_password = fake.password()
        self.form_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "cpf": get_only_numbers(fake.cpf()),
            "is_staff": True,
            "password_1": self.fake_password,
            "password_2": self.fake_password,
        }

    def test_custom_user_creation_form_successfully(self):
        # Given in setUp

        # When
        form = CustomUserCreationForm(data=self.form_data)

        # Then
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_with_invalid_cpf(self):
        # Given
        form_data = self.form_data
        form_data["cpf"] = "00000000000"
        expected_error = ["CPF digitado é inválido"]

        # When
        form = CustomUserCreationForm(data=form_data)

        # Then
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["cpf"], expected_error)

    def test_custom_user_creation_form_with_passwords_not_matching(self):
        # Given
        form_data = self.form_data
        form_data["password_2"] = fake.password()

        # When
        form = CustomUserCreationForm(data=form_data)

        # Then
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password_2"], ["Passwords don't match"])
