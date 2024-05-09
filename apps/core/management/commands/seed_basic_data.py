import json
from uuid import uuid4

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from apps.address_manager.models import City, State
from apps.core.models import CustomUser
from apps.core.utils.regex_utils import get_only_numbers
from apps.ride_manager.models import Person, PhoneValidation
from apps.term_manager.enums import TermTypeChoices
from apps.term_manager.models import Term

fake = Faker("pt_BR")


class Command(BaseCommand):
    help = "Seeds the database with basic data"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            self.seed_states()
            self.seed_cities()
            self.seed_terms()
            self.seed_phone_validations()
            self.seed_persons()

            self.stdout.write(self.style.SUCCESS("Database has been seeded"))

    def seed_states(self) -> None:
        with open("apps/core/management/commands/states.json") as file:
            states = json.load(file)
            for state in states:
                State.objects.create(**state)
            self.stdout.write(self.style.SUCCESS("States data has been seeded"))

    def seed_cities(self) -> None:
        with open("apps/core/management/commands/cities_by_state.json") as file:
            cities_data = json.load(file)

            for state_name, cities in cities_data.items():
                state = State.objects.get(name=state_name)

                for city in cities:
                    City.objects.create(name=city, state=state)

            self.stdout.write(self.style.SUCCESS("Cities data has been seeded"))

    def seed_terms(self) -> None:
        terms = [
            {
                "type": TermTypeChoices.USE,
                "content": fake.text(),
                "version": "0.0.0",
            },
            {
                "type": TermTypeChoices.PRIVACY,
                "content": fake.text(),
                "version": "0.0.0",
            },
        ]

        for term in terms:
            Term.objects.create(**term)

        self.stdout.write(self.style.SUCCESS("Terms data has been seeded"))

    def seed_phone_validations(self) -> None:
        PhoneValidation.objects.create(
            integration_sid=str(uuid4()),
            phone=fake.numerify("(##) #####-####"),
            is_active=True,
        )
        self.stdout.write(
            self.style.SUCCESS("Phone validations data has been seeded")
        )

    def seed_persons(self) -> None:
        for _ in range(10):
            user = CustomUser.objects.create_user(
                cpf=get_only_numbers(fake.cpf()),
                password="123456",
            )
            cities = City.objects.all()

            Person.objects.create(
                user=user,
                name=fake.name(),
                phone=fake.numerify("(##) #####-####"),
                emergency_phone=fake.numerify("(##) #####-####"),
                emergency_contact=fake.name(),
                birth_date=fake.date_of_birth(),
                city=fake.random_element(cities),
            )
        self.stdout.write(self.style.SUCCESS("Persons data has been seeded"))
