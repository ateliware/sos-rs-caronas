import factory
from faker import Faker

from apps.core.models.custom_user import CustomUser

fake = Faker("pt_BR")


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    is_staff = False
    is_active = True
    is_superuser = False
    password = fake.password()

    @classmethod
    def custom_user_data(cls) -> dict:
        return {
            "first_name": cls.first_name,
            "last_name": cls.last_name,
            "email": cls.email,
            "is_staff": cls.is_staff,
            "is_active": cls.is_active,
            "is_superuser": cls.is_superuser,
            "password": cls.password,
        }
