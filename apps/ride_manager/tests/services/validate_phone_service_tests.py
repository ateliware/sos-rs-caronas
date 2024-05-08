from unittest.mock import Mock, patch
from apps.core.tests.base_test import BaseTest
from apps.ride_manager.services.validate_phone_service import ValidatePhoneService

PATCH = 'apps.ride_manager.services.validate_phone_service.TwilioIntegration'
class TestValidatePhoneService(BaseTest):
    
    @patch(PATCH, autospec=True)
    def test_send_code(self, mock_twilio_integration):
        # Given
        phone_number = "+5511999999999"
        mock_twilio_integration_instance = mock_twilio_integration.return_value
        mock_twilio_integration_instance.send_code.return_value = {
            "status": "pending"
        }

        # When
        service = ValidatePhoneService()
        response = service.send_code(phone_number)

        # Assert
        assert response["status"] == "pending"
        mock_twilio_integration_instance.send_code.assert_called_once_with(phone_number)


    @patch(PATCH, autospec=True)
    def test_is_code_valid(self, mock_twilio_integration):
        # Given
        phone_number = "+5511999999999"
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
        service = ValidatePhoneService()
        response = service.is_code_valid(phone_number, code, service_sid)

        # Assert
        assert response["status"] == "approved"
        mock_twilio_integration_instance.is_code_valid.assert_called_once_with(phone_number, code, service_sid)