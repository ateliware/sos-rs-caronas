import io
from copy import deepcopy

from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from PIL import Image

from apps.core.utils.regex_utils import get_only_numbers
from apps.ride_manager.tests.factories.valid_base64_image_factory import (
    valid_base64_image,
)

fake = Faker("pt_BR")


def person_register_payload_factory() -> dict:
    password = fake.password()
    return {
        "cpf": get_only_numbers(fake.cpf()),
        "password": password,
        "password_confirm": password,
        "name": fake.name(),
        "birth_date": fake.date_of_birth(
            minimum_age=18, maximum_age=80
        ).strftime("%Y-%m-%d"),
        "phone": fake.numerify("(##) #####-####"),
        "emergency_phone": fake.numerify("(##) #####-####"),
        "zip_code": fake.numerify(text="#####-###"),
        "lgpd_acceptance": True,
        "avatar": valid_base64_image(),
    }


def person_register_form_data_factory() -> dict:
    password = fake.password()
    return {
        "cpf": get_only_numbers(fake.cpf()),
        "password": password,
        "password_confirmation": password,
        "name": fake.name(),
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "phone": fake.numerify("(##) #####-####"),
        "emergency_phone": fake.numerify("(##) #####-####"),
        "emergency_contact": fake.name(),
        "lgpd_acceptance": True,
    }


def image_file_for_form_factory() -> SimpleUploadedFile:
    image = Image.new("RGB", (100, 100), "white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    file = SimpleUploadedFile(
        "document_picture.jpg",
        content=buffer.getvalue(),
        content_type="image/jpeg",
    )
    return file
