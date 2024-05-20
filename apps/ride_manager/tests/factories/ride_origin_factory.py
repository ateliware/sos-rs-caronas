import factory
from faker import Faker

from apps.ride_manager.models.ride_origin import RideOrigin

fake = Faker("pt_BR")


class RideOriginFactory(factory.django.DjangoModelFactory):
    name = fake.city()
    is_enabled = True

    @staticmethod
    def ride_origin_data() -> dict:
        return {
            "name": fake.city(),
            "is_enabled": True,
        }

    class Meta:
        model = RideOrigin
