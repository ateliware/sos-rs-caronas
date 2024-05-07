import factory
from faker import Faker

from apps.term_manager.enums import TermTypeChoices
from apps.term_manager.models.term import Term

fake = Faker("pt_BR")


class TermFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Term

    version = fake.numerify(text="##.##.##")
    type = fake.random_element(TermTypeChoices.values)
    content = fake.text()

    @staticmethod
    def term_data():
        return {
            "version": fake.numerify(text="##.##.##"),
            "type": fake.random_element(TermTypeChoices.values),
            "content": fake.text(),
        }
