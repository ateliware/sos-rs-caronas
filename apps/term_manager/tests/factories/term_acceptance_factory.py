import factory
from faker import Faker

from apps.core.tests.factories.custom_user_factory import CustomUserFactory
from apps.term_manager.models.term_acceptance import TermAcceptance
from apps.term_manager.tests.factories.term_factory import TermFactory

fake = Faker("pt_BR")


class TermAcceptanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TermAcceptance

    term = factory.SubFactory(TermFactory)
    user = factory.SubFactory(CustomUserFactory)
