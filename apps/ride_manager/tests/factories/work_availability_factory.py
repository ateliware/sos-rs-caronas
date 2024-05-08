import factory
from faker import Faker

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.ride_manager.models import WorkAvailability
from apps.ride_manager.tests.factories.affected_place_factory import (
    AffectedPlaceFactory,
)
from apps.ride_manager.tests.factories.person_factory import PersonFactory

fake = Faker("pt_BR")


class WorkAvailabilityFactory(factory.django.DjangoModelFactory):
    person = factory.SubFactory(PersonFactory)
    origin = factory.SubFactory(CityFactory)
    destination = factory.SubFactory(AffectedPlaceFactory)
    date = fake.date_this_year()

    class Meta:
        model = WorkAvailability
