from unittest.mock import MagicMock, patch

from rest_framework import status

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.models.phone_validation import PhoneValidation
from apps.ride_manager.tests.factories.phone_validation_factory import (
    PhoneValidationFactory,
)

PATCH_PATH = (
    "apps.ride_manager.apis.validate_phone_check_code.CodeValidatorService"
)


class ValidatePhoneAPIViewTestCase(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = "/api/v1/validate_phone/check_code/"

    @patch(PATCH_PATH)
    def test_post_method_success(self, mock_service):
        # Given
        phone_validation = PhoneValidationFactory()
        data = {
            "phone": phone_validation.phone,
            "code": "132456",
            "validation_uuid": phone_validation.uuid,
        }
        mock_object = mock_service.return_value
        mock_object.is_code_valid.return_value = True

        # When
        response = self.unauth_client.post(
            self.url,
            data=data,
            format="json",
        )
        db_phone_validation = PhoneValidation.objects.get(
            uuid=phone_validation.uuid
        )

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Código validado com sucesso."
        )
        self.assertTrue(db_phone_validation.is_active)

    @patch(PATCH_PATH)
    def test_post_method_when_code_is_not_valid(self, mock_service):
        # Given
        phone_validation = PhoneValidationFactory()
        data = {
            "phone": phone_validation.phone,
            "code": "132456",
            "validation_uuid": phone_validation.uuid,
        }
        mock_object = mock_service.return_value
        mock_object.is_code_valid.return_value = False

        # When
        response = self.unauth_client.post(
            self.url,
            data=data,
            format="json",
        )
        db_phone_validation = PhoneValidation.objects.get(
            uuid=phone_validation.uuid
        )

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Código inválido.")
        self.assertFalse(db_phone_validation.is_active)

    def test_post_method_missing_payload_data(self):
        # Given
        # no payload data

        # When
        response = self.unauth_client.post(
            self.url,
            data={},
            format="json",
        )

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Erro ao validar os dados.")

        required_fields = ["phone", "code", "validation_uuid"]
        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(field, response.data["errors"])

    def test_post_method_when_validation_phone_not_found(self):
        # Given
        data = {
            "phone": self.fake.numerify(text="###########"),
            "code": "132456",
            "validation_uuid": self.fake.uuid4(),
        }

        # When
        response = self.unauth_client.post(
            self.url,
            data=data,
            format="json",
        )

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["message"], "UUID de validação não encontrado."
        )
