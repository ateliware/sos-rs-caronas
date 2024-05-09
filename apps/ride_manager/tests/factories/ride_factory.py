import factory
from faker import Faker

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.ride_manager.models.ride import Ride, ShiftChoices, StatusChoices
from apps.ride_manager.tests.factories.affected_place_factory import (
    AffectedPlaceFactory,
)
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.vehicle_factory import VehicleFactory

fake = Faker("pt_BR")


class RideFactory(factory.django.DjangoModelFactory):
    uuid = fake.uuid4()
    date = fake.date()
    work_shift = fake.random_element(ShiftChoices.values)
    origin = factory.SubFactory(CityFactory)
    destination = factory.SubFactory(AffectedPlaceFactory)
    driver = factory.SubFactory(PersonFactory)
    vehicle = factory.SubFactory(VehicleFactory)
    notes = fake.text()
    status = fake.random_element(StatusChoices.values)
    is_active = fake.boolean()

    @staticmethod
    def ride_data() -> dict:
        return {
            "uuid": fake.uuid4(),
            "date": fake.date(),
            "work_shift": fake.random_element(ShiftChoices.values),
            "origin": CityFactory.city_data(),
            "destination": AffectedPlaceFactory.affected_place_data(),
            "driver": PersonFactory.person_data(),
            "vehicle": VehicleFactory.vehicle_data(),
            "notes": fake.text(),
            "status": fake.random_element(StatusChoices.values),
            "is_active": fake.boolean(),
        }

    class Meta:
        model = Ride
