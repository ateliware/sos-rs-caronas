import factory
from faker import Faker

from apps.address_manager.models.city import City
from apps.address_manager.tests.factories.state_factory import StateFactory

fake = Faker("pt_BR")


class CityFactory(factory.django.DjangoModelFactory):
    name = fake.city()
    state = factory.SubFactory(StateFactory)

    @staticmethod
    def city_data() -> dict:
        return {
            "name": fake.city(),
            "state_code": StateFactory.state_data()["code"],
        }

    class Meta:
        model = City
