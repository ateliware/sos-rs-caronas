import io
from copy import deepcopy
from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.base_test import BaseTest
from apps.ride_manager.forms import RegistrationForm
from apps.ride_manager.tests.factories.person_register_payload_factory import (
    image_file_for_form_factory,
    person_register_form_data_factory,
    person_register_payload_factory,
)


class RegistrationFormTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.city = CityFactory()
        self.form_data = person_register_form_data_factory()
        self.form_data["city_id"] = self.city.id
        self.form_data["state_id"] = self.city.state.id
        self.document_picture = image_file_for_form_factory()
        self.form_data["document_picture"] = self.document_picture

    def test_placeholder_and_label(self):
        # Given
        form = RegistrationForm()

        # Then
        for field_name, (label, placeholder) in form.field_labels.items():
            self.assertEqual(form.fields[field_name].label, label)
            self.assertEqual(
                form.fields[field_name].widget.attrs["placeholder"], placeholder
            )

    def test_form_valid(self):
        # Given
        form = RegistrationForm(
            self.form_data, {"document_picture": self.document_picture}
        )

        # When
        is_valid = form.is_valid()

        # Then
        self.assertTrue(is_valid)

    def test_form_invalid_when_cpf_is_empty(self):
        # Given
        form_data = deepcopy(self.form_data)
        form_data["cpf"] = None
        form = RegistrationForm(
            form_data, {"document_picture": self.document_picture}
        )
        expected_error = "Este campo é obrigatório."

        # When
        is_valid = form.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn(expected_error, form.errors.get("cpf")[0])

    def test_form_invalid_when_cpf_is_invalid(self):
        # Given
        form_data = deepcopy(self.form_data)
        form_data["cpf"] = "12345678901"
        form = RegistrationForm(
            form_data, {"document_picture": self.document_picture}
        )
        expected_error = "CPF inválido"

        # When
        is_valid = form.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn(expected_error, form.errors.get("cpf")[0])

    def test_form_invalid_when_cpf_is_registered(self):
        # Given
        form_data = deepcopy(self.form_data)
        form_data["cpf"] = self.user.cpf
        form = RegistrationForm(
            form_data, {"document_picture": self.document_picture}
        )
        expected_error = "CPF já cadastrado"

        # When
        is_valid = form.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn(expected_error, form.errors.get("cpf")[0])

    def test_form_invalid_when_password_confirmation_is_different(self):
        # Given
        form_data = deepcopy(self.form_data)
        form_data["password_confirmation"] = "123456"
        form = RegistrationForm(
            form_data, {"document_picture": self.document_picture}
        )
        expected_error = "Senhas não conferem"

        # When
        is_valid = form.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn(
            expected_error, form.errors.get("password_confirmation")[0]
        )

    def test_form_invalid_when_lgpd_acceptance_is_false(self):
        # Given
        form_data = deepcopy(self.form_data)
        form_data["lgpd_acceptance"] = False
        form = RegistrationForm(
            form_data, {"document_picture": self.document_picture}
        )
        expected_error = "Este campo é obrigatório."

        # When
        is_valid = form.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn(expected_error, form.errors.get("lgpd_acceptance")[0])

    def test_form_invalid_when_birth_date_is_less_than_18_years(self):
        # Given
        form_data = deepcopy(self.form_data)
        form_data["birth_date"] = date.today().strftime("%Y-%m-%d")
        form = RegistrationForm(
            form_data, {"document_picture": self.document_picture}
        )
        expected_error = "Você deve ter mais de 18 anos para se cadastrar"

        # When
        is_valid = form.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn(expected_error, form.errors.get("birth_date")[0])

    def test_form_invalid_when_document_picture_is_empty(self):
        # Given
        form_data = deepcopy(self.form_data)
        form = RegistrationForm(form_data)
        expected_error = "Este campo é obrigatório."

        # When
        is_valid = form.is_valid()

        # Then
        self.assertFalse(is_valid)
        self.assertIn(expected_error, form.errors.get("document_picture")[0])
