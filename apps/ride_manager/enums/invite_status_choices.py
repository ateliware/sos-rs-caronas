from django.db import models


class InviteStatusChoices(models.TextChoices):
    PENDING = ("PENDING", "Pendente")
    ACCEPTED = ("ACCEPTED", "Aceito")
    REFUSED = ("REFUSED", "Recusado")
