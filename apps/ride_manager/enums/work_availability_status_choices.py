from django.db import models


class WorkAvailabilityStatusChoices(models.TextChoices):
    OPEN = ("OPEN", "Disponível")
    IN_RESERVATION = ("IN_RESERVATION", "Combinando viagem")
    CLOSED = ("CLOSED", "Concluído")
