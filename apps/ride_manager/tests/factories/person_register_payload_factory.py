from faker import Faker

from apps.client_manager.tests.factories.valid_base64_image_factory import (
    valid_base64_image,
)
from apps.core.utils.regex_utils import get_only_numbers

fake = Faker("pt_BR")


def person_register_payload_factory() -> dict:
    password = fake.password()
    return {
        "cpf": get_only_numbers(fake.cpf()),
        "password": password,
        "password_confirm": password,
        "name": fake.name(),
        "birth_date": fake.date(),
        "phone": fake.numerify("(##) #####-####"),
        "emergency_phone": fake.numerify("(##) #####-####"),
        "zip_code": fake.numerify(text="#####-###"),
        "lgpd_acceptance": True,
        "avatar": valid_base64_image(),
    }
