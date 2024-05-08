import logging

from decouple import config
from twilio.rest import Client


class TwilioIntegration:

    def __init__(self):
        self.client = self.create_twilio_service()

    def create_twilio_service(self):
        account_sid = config("TWILIO_ACCOUNT_SID")
        auth_token = config("TWILIO_AUTH_TOKEN")

        try:
            return Client(account_sid, auth_token)
        except Exception as error:
            logging.error(
                f"Error when try to create a service with integration service, with message: {error}"
            )

    def send_code(self, to_number):
        service = self.client.verify.v2.services.create(
            friendly_name="Código de Verificação"
        )

        try:
            verification = self.client.verify.v2.services(
                service.sid
            ).verifications.create(to=to_number, channel="sms")
        except Exception as error:
            logging.error(
                f"Error when try to create verification service with message: {error}"
            )
            return None
        return verification

    def is_code_valid(self, to_number, code, service_sid):
        verification_check = self.client.verify.v2.services(
            service_sid
        ).verification_checks.create(to=to_number, code=code)
        return verification_check.valid
