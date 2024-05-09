from twilio.rest import Client as TwilioClient

from apps.core.utils.regex_utils import get_only_numbers
from apps.ride_manager.services.twilio_integration_service import (
    TwilioIntegration,
)

COUNTRY_CODE = "+55"


class CodeValidatorService:
    def __init__(self):
        self.integration = TwilioIntegration()

    def send_code(self, to_number: str) -> TwilioClient:
        to_number = self.normalize_phone_number(to_number)
        return self.integration.send_code(to_number)

    def is_code_valid(
        self, to_number: str, code: str, service_sid: str
    ) -> bool:
        to_number = self.normalize_phone_number(to_number)
        return self.integration.is_code_valid(to_number, code, service_sid)

    def normalize_phone_number(self, phone_number: str) -> str:
        only_numbers = get_only_numbers(phone_number)
        return f"{COUNTRY_CODE}{only_numbers}"
