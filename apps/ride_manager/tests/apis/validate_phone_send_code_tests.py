from unittest.mock import MagicMock, patch

from rest_framework import status

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.models.phone_validation import PhoneValidation

PATCH_PATH = (
    "apps.ride_manager.apis.validate_phone_send_code.CodeValidatorService"
)


class ValidatePhoneAPIViewTestCase(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = "/api/v1/validate_phone/send_code/"

    @patch(PATCH_PATH)
    def test_post_method_success(self, mock_service):
        # Given
        data = {"phone": "54999999999"}
        mock_response = MagicMock(service_sid="mocked_sid")
        mock_object = mock_service.return_value
        mock_object.send_code.return_value = mock_response

        # When
        response = self.unauth_client.post(
            self.url,
            data=data,
            format="json",
        )

        # Then
        phone_validation = PhoneValidation.objects.get(
            integration_sid="mocked_sid"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Código Enviado.")
        self.assertEqual(
            response.data["validation_uuid"], str(phone_validation.uuid)
        )
        self.assertFalse(phone_validation.is_active)

    @patch(PATCH_PATH)
    def test_post_method_missing_phone(self, mock_service):
        # Given
        mock_response = MagicMock(service_sid="mocked_sid")
        mock_object = mock_service.return_value
        mock_object.send_code.return_value = mock_response

        # When
        response = self.unauth_client.post(
            self.url,
            data={},
            format="json",
        )

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Erro ao validar os dados.")

        required_fields = ["phone"]
        for field in required_fields:
            self.assertIn(field, response.data["errors"])
