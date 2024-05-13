from apps.core.tests.base_test import FAKE_CPF, BaseTest
from apps.core.utils.regex_utils import get_only_numbers
from apps.ride_manager.forms import CustomLoginForm


class CustomLoginViewTests(BaseTest):
    def test_clean_cpf_when_cpf_is_valid(self):
        # Given
        new_cpf = self.fake.cpf()
        self.create_test_user(
            cpf=new_cpf,
            password="testpassword",
        )
        form_data = {
            "cpf": new_cpf,
            "password": "testpassword",
        }
        expected_response = get_only_numbers(new_cpf)

        # When
        form = CustomLoginForm(data=form_data)

        # Then
        form_is_valid = form.is_valid()
        cleaned_cpf = form.cleaned_data.get("cpf")
        self.assertTrue(form_is_valid)
        self.assertEqual(cleaned_cpf, expected_response)

    def test_validation_raise_errors_when_user_not_found(self):
        # Given
        form_data = {
            "cpf": self.fake.cpf(),
            "password": "testpassword",
        }
        expected_message = "CPF ou senha inválidos"

        # When
        form = CustomLoginForm(data=form_data)

        # Then
        form_is_valid = form.is_valid()
        self.assertFalse(form_is_valid)
        self.assertIn(expected_message, form.errors.get("__all__"))

    def test_validation_raise_errors_when_password_is_wrong(self):
        # Given
        form_data = {
            "cpf": FAKE_CPF,
            "password": "wrongpassword",
        }
        expected_message = "CPF ou senha inválidos"

        # When
        form = CustomLoginForm(data=form_data)

        # Then
        form_is_valid = form.is_valid()
        self.assertFalse(form_is_valid)
        self.assertIn(expected_message, form.errors.get("__all__"))

    def test_validation_raise_errors_when_cpf_is_empty(self):
        # Given
        form_data = {
            "cpf": "",
            "password": "testpassword",
        }
        expected_message = "Este campo é obrigatório."

        # When
        form = CustomLoginForm(data=form_data)

        # Then
        form_is_valid = form.is_valid()
        obtained_message = form.errors.get("cpf")[0]
        self.assertFalse(form_is_valid)
        self.assertEqual(expected_message, obtained_message)

    def test_validation_raise_errors_when_password_is_empty(self):
        # Given
        form_data = {
            "cpf": FAKE_CPF,
            "password": "",
        }
        expected_message = "Este campo é obrigatório."

        # When
        form = CustomLoginForm(data=form_data)

        # Then
        form_is_valid = form.is_valid()
        obtained_message = form.errors.get("password")[0]
        self.assertFalse(form_is_valid)
        self.assertEqual(expected_message, obtained_message)
