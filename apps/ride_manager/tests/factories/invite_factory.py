import factory
from faker import Faker

from apps.ride_manager.models import Invite
from apps.ride_manager.tests.factories.ride_factory import RideFactory
from apps.ride_manager.tests.factories.voluntary_factory import VoluntaryFactory

fake = Faker("pt_BR")


class InviteFactory(factory.django.DjangoModelFactory):
    ride = factory.SubFactory(RideFactory)
    voluntary = factory.SubFactory(VoluntaryFactory)

    class Meta:
        model = Invite
