import factory
from faker import Faker

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.factories.custom_user_factory import CustomUserFactory
from apps.ride_manager.models.person import Person

fake = Faker("pt_BR")


class PersonFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(CustomUserFactory)
    name = fake.name()
    phone = fake.numerify("(##) #####-####")
    emergency_phone = fake.numerify("(##) #####-####")
    emergency_contact = fake.name()
    birth_date = fake.date_of_birth()
    avatar = fake.file_name()
    cnh_picture = fake.file_name()
    document_picture = fake.file_name()
    cnh_number = fake.numerify("###########")
    city = factory.SubFactory(CityFactory)
    zip_code = fake.numerify("#####-###")

    @staticmethod
    def person_data() -> dict:
        return {
            "name": fake.name(),
            "phone": fake.numerify("(##) #####-####"),
            "emergency_phone": fake.numerify("(##) #####-####"),
            "emergency_contact": fake.name(),
            "birth_date": fake.date_of_birth(),
            "avatar": fake.file_name(),
            "cnh_picture": fake.file_name(),
            "document_picture": fake.file_name(),
            "cnh_number": fake.numerify("###########"),
            "zip_code": fake.numerify("#####-###"),
        }

    class Meta:
        model = Person
