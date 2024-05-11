import factory
from faker import Faker

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.ride_manager.enums import (
    VoluntaryAvailabilityStatusChoices,
    WorkShiftChoices,
)
from apps.ride_manager.models import Voluntary
from apps.ride_manager.tests.factories.affected_place_factory import (
    AffectedPlaceFactory,
)
from apps.ride_manager.tests.factories.person_factory import PersonFactory

fake = Faker("pt_BR")


class VoluntaryFactory(factory.django.DjangoModelFactory):
    person = factory.SubFactory(PersonFactory)
    origin = factory.SubFactory(CityFactory)
    destination = factory.SubFactory(AffectedPlaceFactory)
    date = fake.date_this_year()
    any_destination = fake.boolean()
    work_shift = fake.random_element(WorkShiftChoices.values)

    @staticmethod
    def voluntary_data() -> dict:
        return {
            "origin": CityFactory().pk,
            "destination": AffectedPlaceFactory().pk,
            "any_destination": fake.boolean(),
            "date": fake.date_this_year(),
            "work_shift": fake.random_element(WorkShiftChoices.values),
        }

    class Meta:
        model = Voluntary
