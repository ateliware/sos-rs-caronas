import json

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from apps.address_manager.models import City, State
from apps.ride_manager.models import (
    AffectedPlace,
)

fake = Faker("pt_BR")


class Command(BaseCommand):
    help = "Seeds the database with basic data for prod"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            self.seed_states()
            self.seed_cities()
            self.seed_affected_places()
            self.stdout.write(self.style.SUCCESS("Database has been seeded"))

    def seed_states(self) -> None:
        with open("apps/core/management/commands/states.json") as file:
            states = json.load(file)
            for state in states:
                has_state = State.objects.filter(name=state["name"]).exists()
                if not has_state:
                    State.objects.create(**state)
            self.stdout.write(self.style.SUCCESS("States data has been seeded"))

    def seed_cities(self) -> None:
        with open("apps/core/management/commands/cities_by_state.json") as file:
            cities_data = json.load(file)

            for state_name, cities in cities_data.items():
                state = State.objects.get(name=state_name)

                for city in cities:
                    has_city = City.objects.filter(
                        name=city, state=state
                    ).exists()
                    if not has_city:
                        City.objects.create(name=city, state=state)

            self.stdout.write(self.style.SUCCESS("Cities data has been seeded"))

    def seed_affected_places(self) -> None:
        cities = [
            "Candelária",
            "Encruzilhada do Sul",
            "Gramado Xavier",
            "Herveiras",
            "Mato Leitão",
            "Pantano Grande",
            "Passo do Sobrado",
            "Rio Pardo",
            "Santa Cruz do Sul",
            "Sinimbu",
            "Vale do Sol",
            "Vale Verde",
            "Venâncio Aires",
            "Vera Cruz",
            "Arroio do Meio",
            "Bom Retiro do Sul",
            "Boqueirão do Leão",
            "Canudos do Vale",
            "Capitão",
            "Colinas",
            "Coqueiro Baixo",
            "Cruzeiro do Sul",
            "Estrela",
            "Fazenda Vilanova",
            "Forquetinha",
            "Imigrante",
            "Lajeado",
            "Marques de Souza",
            "Paverama",
            "Poço das Antas",
            "Pouso Novo",
            "Progresso",
            "Santa Clara do Sul",
            "Sério",
            "Tabaí",
            "Taquari",
            "Teutônia",
            "Travesseiro",
            "Westfália",
            "Arroio do Tigre",
            "Estrela Velha",
            "Ibarama",
            "Lagoa Bonita do Sul",
            "Lagoão",
            "Passa-Sete",
            "Segredo",
            "Sobradinho",
            "Tunas",
            "Anta Gorda",
            "Doutor Ricardo",
            "Encantado",
            "Ilópolis",
            "Muçum",
            "Nova Bréscia",
            "Putinga",
            "Relvado",
            "Roca Sales",
            "Vespasiano Corrêa",
        ]

        for city_name in cities:
            city = City.objects.filter(name=city_name).first()
            if not city:
                state = State.objects.get(name="Rio Grande do Sul")
                city = City.objects.create(
                    name=city_name,
                    state=state,
                )
            AffectedPlace.objects.create(
                description="Em breve mais informações",
                informations="Em breve mais informações",
                address="Em breve mais informações",
                city=city,
                main_person="Em breve mais informações",
                main_contact="Em breve mais informações",
                is_active=False,
            )
        self.stdout.write(
            self.style.SUCCESS("Affected places data has been seeded")
        )
