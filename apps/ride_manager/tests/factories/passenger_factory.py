import factory
from faker import Faker

from apps.ride_manager.enums.passenger_status_choices import (
    PassengerStatusChoices,
)
from apps.ride_manager.models.passenger import Passenger
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.ride_factory import RideFactory

fake = Faker("pt_BR")


class PassengerFactory(factory.django.DjangoModelFactory):
    person = factory.SubFactory(PersonFactory)
    ride = factory.SubFactory(RideFactory)
    is_driver = fake.boolean()
    status = fake.random_element(PassengerStatusChoices.values)

    @staticmethod
    def passenger_data() -> dict:
        return {
            "person": PersonFactory.person_data(),
            "ride": RideFactory.ride_data(),
            "is_driver": fake.boolean(),
            "status": fake.random_element(PassengerStatusChoices.values),
        }

    class Meta:
        model = Passenger
