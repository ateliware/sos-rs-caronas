import factory
from faker import Faker

from apps.address_manager.models.state import State

fake = Faker("pt_BR")


class StateFactory(factory.django.DjangoModelFactory):
    name = fake.state()
    code = fake.state_abbr()

    @staticmethod
    def state_data() -> dict:
        return {
            "name": fake.state(),
            "code": fake.state_abbr(),
        }

    class Meta:
        model = State
