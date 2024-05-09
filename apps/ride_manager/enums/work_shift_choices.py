from django.db import models


class WorkShiftChoices(models.TextChoices):
    MORNING = ("MORNING", "Manhã")
    AFTERNOON = ("AFTERNOON", "Tarde")
    ALL_DAY = ("ALL_DAY", "Dia todo")
