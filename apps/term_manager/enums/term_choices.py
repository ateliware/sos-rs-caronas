from django.db import models


class TermTypeChoices(models.TextChoices):
    USE = (
        "USE",
        "Termo de uso",
    )
    PRIVACY = (
        "PRIVACY",
        "Política de privacidade",
    )
