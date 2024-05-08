from apps.ride_manager.services.validate_phone_service import ValidatePhoneService

class TestValidatePhoneService:
    
    def test_send_code(self):
        # Given
        phone_number = "+5511999999999"

        # When
        service = ValidatePhoneService()        
        response = service.send_code(phone_number)

        # Assert
        assert response.status == "pending"

    def test_is_code_valid(self):
        phone_number = "+5511999999999"
        code = "123456"
        service_sid = "123456"
        service = ValidatePhoneService()
        response = service.is_code_valid(phone_number, code, service_sid)
        assert response.status == "approved"