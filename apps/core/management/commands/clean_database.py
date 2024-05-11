from django.core.management.base import BaseCommand
from django.db import transaction

from apps.address_manager.models import City, State
from apps.core.models import CustomUser
from apps.ride_manager.models import (
    AffectedPlace,
    Invite,
    Passenger,
    Person,
    PhoneValidation,
    Ride,
    Vehicle,
    Voluntary,
)
from apps.term_manager.models import Term, TermAcceptance


class Command(BaseCommand):
    help = "Clean database"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            self.clean_invites()
            self.clean_passengers()
            self.clean_rides()
            self.clean_voluntaries()
            self.clean_vehicles()
            self.clean_terms_acceptances()
            self.clean_terms()
            self.clean_persons()
            self.clean_phone_validations()
            self.clean_affected_places()
            self.clean_cities()
            self.clean_states()
            self.clean_users()
            self.stdout.write(self.style.SUCCESS("Database has been cleaned"))

    def clean_states(self) -> None:
        State.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("States data has been cleaned"))

    def clean_cities(self) -> None:
        City.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Cities data has been cleaned"))

    def clean_terms(self) -> None:
        Term.objects.all().delete()

    def clean_phone_validations(self) -> None:
        PhoneValidation.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS("Phone validations data has been cleaned")
        )

    def clean_persons(self) -> None:
        Person.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Persons data has been cleaned"))

    def clean_vehicles(self) -> None:
        Vehicle.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Vehicles data has been cleaned"))

    def clean_voluntaries(self) -> None:
        Voluntary.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS("Voluntaries data has been cleaned")
        )

    def clean_rides(self) -> None:
        Ride.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Rides data has been cleaned"))

    def clean_passengers(self) -> None:
        Passenger.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS("Passengers data has been cleaned")
        )

    def clean_invites(self) -> None:
        Invite.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Invites data has been cleaned"))

    def clean_affected_places(self) -> None:
        AffectedPlace.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS("Affected places data has been cleaned")
        )

    def clean_users(self) -> None:
        CustomUser.objects.all().exclude(
            is_superuser=True,
        ).delete()
        self.stdout.write(self.style.SUCCESS("Users data has been cleaned"))

    def clean_terms_acceptances(self) -> None:
        TermAcceptance.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS("Terms acceptances data has been cleaned")
        )
