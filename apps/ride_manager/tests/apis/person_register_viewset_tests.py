from copy import deepcopy

from rest_framework import status

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.base_test import BaseTest
from apps.ride_manager.tests.factories.person_register_payload_factory import (
    person_register_payload_factory,
)
from apps.ride_manager.tests.factories.phone_validation_factory import (
    PhoneValidationFactory,
)
from apps.term_manager.enums import TermTypeChoices
from apps.term_manager.tests.factories.term_factory import TermFactory


class PersonRegisterViewSetTests(BaseTest):
    def setUp(self):
        super().setUp()
        TermFactory(type=TermTypeChoices.USE)
        TermFactory(type=TermTypeChoices.PRIVACY)
        self.city = CityFactory()
        self.payload = person_register_payload_factory()
        self.phone_validation = PhoneValidationFactory(
            is_active=True,
            phone=self.payload["phone"],
        )
        self.url = "/api/v1/person/register/"
        self.payload["validation_uuid"] = str(self.phone_validation.uuid)
        self.payload["city_id"] = self.city.id

    def test_register_person_successfully(self):
        # Given
        expected_keys = [
            "uuid",
            "name",
            "phone",
            "emergency_phone",
            "emergency_contact",
            "birth_date",
            "avatar",
        ]

        # When
        response = self.unauth_client.post(
            self.url,
            data=self.payload,
            format="json",
        )

        # Then
        response_data = response.json()
        reponse_main_keys = list(response_data.keys())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, reponse_main_keys)

    def test_register_person_with_invalid_data(self):
        # Given
        invalid_payload = deepcopy(self.payload)
        invalid_payload["cpf"] = "invalid_cpf"
        expected_error = "Erro ao criar usuário"

        # When
        response = self.unauth_client.post(
            self.url,
            data=invalid_payload,
            format="json",
        )

        # Then
        response_data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertIn("errors", response_data)
        self.assertIn(expected_error, response_data["errors"])

    def test_register_person_with_invalid_serializer_validation_data(self):
        # Given
        invalid_payload = deepcopy(self.payload)
        invalid_payload["password_confirm"] = "invalid_password"
        expected_error = "Senhas não conferem."

        # When
        response = self.unauth_client.post(
            self.url,
            data=invalid_payload,
            format="json",
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response_data)
        self.assertIn(
            expected_error, response_data["message"]["password_confirm"]
        )

    def test_register_person_with_invalid_phone_validation(self):
        # Given
        self.phone_validation.is_active = False
        self.phone_validation.save()

        # When
        response = self.unauth_client.post(
            self.url,
            data=self.payload,
            format="json",
        )

        # Then
        response_data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
