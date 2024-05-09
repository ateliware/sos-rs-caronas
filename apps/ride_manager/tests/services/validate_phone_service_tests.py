from unittest.mock import Mock, patch

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.services.code_validator_service import (
    CodeValidatorService,
)

PATCH = "apps.ride_manager.services.code_validator_service.TwilioIntegration"


class TestCodeValidatorService(BaseTest):

    @patch(PATCH, autospec=True)
    def test_send_code(self, mock_twilio_integration):
        # Given
        phone_number = "(54) 99999-9999"
        mock_twilio_integration_instance = mock_twilio_integration.return_value
        mock_twilio_integration_instance.send_code.return_value = {
            "status": "pending"
        }

        # When
        service = CodeValidatorService()
        response = service.send_code(phone_number)

        # Assert
        assert response["status"] == "pending"
        mock_twilio_integration_instance.send_code.assert_called_once_with(
            "+5554999999999"
        )

    @patch(PATCH, autospec=True)
    def test_is_code_valid(self, mock_twilio_integration):
        # Given
        phone_number = "(54) 99999-9999"
        code = "123456"
        service_sid = "123456"
        mock_twilio_integration_instance = mock_twilio_integration.return_value
        mock_twilio_integration_instance.is_code_valid.return_value = {
            "status": "approved"
        }

        # When
        mock_twilio_integration = Mock()
        mock_twilio_integration.is_code_valid.return_value = {
            "status": "approved"
        }
        service = CodeValidatorService()
        response = service.is_code_valid(phone_number, code, service_sid)

        # Assert
        assert response["status"] == "approved"
        mock_twilio_integration_instance.is_code_valid.assert_called_once_with(
            "+5554999999999", code, service_sid
        )
