import factory
from faker import Faker

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.ride_manager.models.ride_origin import RideOrigin

fake = Faker("pt_BR")


class RideOriginFactory(factory.django.DjangoModelFactory):
    city = factory.SubFactory(CityFactory)
    enabled = True

    @staticmethod
    def ride_origin_data() -> dict:
        return {
            "city": factory.SubFactory(CityFactory),
            "enabled": True,
        }

    class Meta:
        model = RideOrigin
