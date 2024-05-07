import factory
from faker import Faker

from apps.address_manager.models.address import Address
from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.factories.custom_user_factory import CustomUserFactory

fake = Faker("pt_BR")


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    street = fake.street_name()
    number = fake.building_number()
    complement = fake.text()
    neighborhood = fake.neighborhood()
    city = factory.SubFactory(CityFactory)
    zip_code = fake.numerify(text="#####-###")
    description = fake.text()
    user = factory.SubFactory(CustomUserFactory)

    @staticmethod
    def address_data() -> dict:
        return {
            "street": fake.street_name(),
            "number": fake.building_number(),
            "complement": fake.text(),
            "neighborhood": fake.neighborhood(),
            "zip_code": fake.numerify(text="#####-###"),
            "description": fake.text(),
        }
