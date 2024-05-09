from django.db import models


class VoluntaryAvailabilityStatusChoices(models.TextChoices):
    OPEN = ("OPEN", "Disponível")
    IN_RESERVATION = ("IN_RESERVATION", "Combinando viagem")
    CLOSED = ("CLOSED", "Concluído")
