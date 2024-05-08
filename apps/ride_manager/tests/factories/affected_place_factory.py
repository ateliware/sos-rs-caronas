import factory
from faker import Faker

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.ride_manager.models.affected_place import AffectedPlace

fake = Faker("pt_BR")


class AffectedPlaceFactory(factory.django.DjangoModelFactory):
    city = factory.SubFactory(CityFactory)
    main_person = fake.name()
    main_contact = fake.name()
    address = fake.address()
    informations = fake.text()

    @staticmethod
    def affected_place_data() -> dict:
        return {
            "city": CityFactory.city_data(),
            "main_person": fake.name(),
            "main_contact": fake.phone_number(),
            "address": fake.address(),
            "informations": fake.text(),
        }

    class Meta:
        model = AffectedPlace
