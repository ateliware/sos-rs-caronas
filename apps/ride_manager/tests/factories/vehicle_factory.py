import base64

import factory
from django.core.files.base import ContentFile
from faker import Faker

from apps.ride_manager.models import Vehicle
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.valid_base64_image_factory import (
    valid_base64_image,
)

fake = Faker("pt_BR")


class VehicleFactory(factory.django.DjangoModelFactory):
    model = fake.name()
    color = fake.color_name()
    plate = fake.license_plate()
    plate_picture = factory.django.ImageField(filename="plate_picture.jpg")
    vehicle_picture = factory.django.ImageField(filename="vehicle_picture.jpg")
    is_verified = fake.boolean()
    person = factory.SubFactory(PersonFactory)

    @staticmethod
    def vehicle_data() -> dict:
        return {
            "model": fake.name(),
            "color": fake.color_name(),
            "plate": fake.license_plate(),
            "plate_picture": ContentFile(
                base64.b64decode(valid_base64_image()),
                name="plate_picture.jpg",
            ),
            "vehicle_picture": ContentFile(
                base64.b64decode(valid_base64_image()),
                name="plate_picture.jpg",
            ),
            "is_verified": fake.boolean(),
        }

    class Meta:
        model = Vehicle
