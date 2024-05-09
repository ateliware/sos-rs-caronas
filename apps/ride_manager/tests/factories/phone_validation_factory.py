import factory
from faker import Faker

from apps.ride_manager.models.phone_validation import PhoneValidation

fake = Faker("pt_BR")


class PhoneValidationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PhoneValidation

    uuid = str(fake.uuid4())
    integration_sid = str(fake.uuid4())
    phone = fake.numerify("(##) #####-####")
    is_active = False

    @classmethod
    def phone_validation_data(cls) -> dict:
        return {
            "uuid": cls.uuid,
            "integration_sid": cls.integration_sid,
            "phone": cls.phone,
            "is_active": cls.is_active,
        }
