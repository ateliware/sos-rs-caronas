import logging

from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404

from apps.address_manager.models import City
from apps.core.models import CustomUser
from apps.ride_manager.models.person import Person
from apps.ride_manager.models.phone_validation import PhoneValidation
from apps.ride_manager.serializers.person_register_serializers import (
    PersonModelSerializer,
)
from apps.term_manager.enums.term_choices import TermTypeChoices
from apps.term_manager.models import Term, TermAcceptance


class PersonRegisterService:
    def __init__(self, data: dict) -> None:
        self.data = data

    def register_person(self) -> dict:
        with transaction.atomic():
            user = self.create_custom_user()
            person = self.create_person(user)
            self.create_acceptance_terms(person)
            response = PersonModelSerializer(person)
            return response.data

    def check_phone_validation(self) -> bool:
        try:
            phone_validation = get_object_or_404(
                PhoneValidation,
                phone=self.data["phone"],
                uuid=self.data["validation_uuid"],
            )
            return phone_validation.is_active

        except Http404:
            raise Exception("Código de validação inválido.")

    def create_custom_user(self) -> CustomUser:
        try:
            user = CustomUser.objects.create_user(
                cpf=self.data["cpf"],
                password=self.data["password"],
            )
            splitted_names = self.data["name"].split(" ")
            user.first_name = splitted_names[0].capitalize()
            user.last_name = splitted_names[-1].capitalize()
            user.email = self.data.get("email")
            user.save()
            return user

        except Exception as e:
            logging.error(f"Error creating user: {e}")
            raise Exception(f"Erro ao criar usuário: {e}")

    def create_person(self, user: CustomUser) -> Person:
        try:
            city = get_object_or_404(City, id=self.data["city_id"])
            person_data = {
                "user": user.pk,
                "name": self.data["name"],
                "phone": self.data["phone"],
                "emergency_phone": self.data.get("emergency_phone"),
                "emergency_contact": self.data.get("emergency_contact"),
                "birth_date": self.data["birth_date"],
                "avatar": self.data.get("avatar"),
                "city": city.pk,
            }
            if person_data["avatar"] is None:
                del person_data["avatar"]

            person_serializer = PersonModelSerializer(data=person_data)
            person_serializer.is_valid(raise_exception=True)
            person = person_serializer.save()
            return person

        except Exception as e:
            logging.error(f"Error creating person: {e}")
            raise Exception(f"Erro ao criar Pessoa: {e}")

    def create_acceptance_terms(self, person: Person) -> list[TermAcceptance]:
        try:
            term_types = [TermTypeChoices.PRIVACY, TermTypeChoices.USE]
            acceptance_terms = list()

            for term_type in term_types:
                term = (
                    Term.objects.filter(
                        type=term_type,
                    )
                    .order_by("-created_at")
                    .first()
                )

                if not term:
                    raise Exception("Termo não encontrado")

                acceptance = TermAcceptance.objects.create(
                    user=person.user,
                    term=term,
                )
                acceptance_terms.append(acceptance)

            return acceptance_terms

        except Exception as e:
            logging.error(f"Error creating acceptance terms: {e}")
            raise Exception(f"Erro ao criar termos de aceite: {e}")
