import factory
from faker import Faker

from apps.ride_manager.models import Vehicle
from apps.ride_manager.tests.factories.person_factory import PersonFactory

fake = Faker("pt_BR")

class VehicleFactory(factory.django.DjangoModelFactory):
    model = fake.name()
    color = fake.color_name()
    plate = fake.license_plate()
    plate_picture = factory.django.ImageField(filename='plate_picture.jpg')
    vehicle_picture = factory.django.ImageField(filename='vehicle_picture.jpg')
    is_verified = fake.boolean()
    person = factory.SubFactory(PersonFactory)

    class Meta:
        model = Vehicle
