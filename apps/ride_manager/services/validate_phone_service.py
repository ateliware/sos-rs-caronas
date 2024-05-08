from .twilio_integration_service import TwilioIntegration

class ValidatePhoneService:
    def __init__(self):
        self.twilio_integration = TwilioIntegration()

    def send_code(self, phone_number):
        return self.twilio_integration.send_code(phone_number)

    def is_code_valid(self, phone_number, code, service_sid):
        return self.twilio_integration.is_code_valid(phone_number, code, service_sid)
    
