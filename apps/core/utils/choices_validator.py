from django.db import models


def validate_choice(value: str, choice_class: models.TextChoices) -> bool:
    valid_choices = list(dict(choice_class.choices).keys())
    return value in valid_choices
