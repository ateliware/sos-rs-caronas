from django.db import models


class ShiftChoices(models.TextChoices):
    MORNING = "MORNING", "Manhã"
    AFTERNOON = "AFTERNOON", "Tarde"


class StatusChoices(models.TextChoices):
    OPEN = "OPEN", "Aberta"
    UNDER_REVIEW = "UNDER_REVIEW", "Em análise"
    CROWDED = "CROWDED", "Lotada"
    FINISHED = "FINISHED", "Concluída"
