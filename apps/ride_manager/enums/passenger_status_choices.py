from django.db import models


class PassengerStatusChoices(models.TextChoices):
    ACCEPTED = "ACCEPTED", "Aceito"
    REJECTED = "DECLINED", "Recusado"
    PENDING = "PENDING", "Pendente"