from uuid import uuid4

from django.db import models

from apps.core.models.base_model import BaseModel
from apps.ride_manager.models.person import Person
from apps.ride_manager.models.ride import Ride


class StatusChoices(models.TextChoices):
    ACCEPTED = "ACCEPTED", "Aceito"
    REJECTED = "DECLINED", "Recusado"


class Passenger(BaseModel):
    class Meta:
        verbose_name = "Passageiro"
        verbose_name_plural = "Passageiros"

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid4,
        primary_key=True,
        editable=False,
        unique=True,
    )
    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        verbose_name="Carona",
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name="Passageiro",
    )
    is_driver = models.BooleanField(
        verbose_name="É Motorista",
    )
    status = models.CharField(
        max_length=255,
        verbose_name="Status",
        choices=StatusChoices.choices,
    )

    def __str__(self):
        return f"{self.person} - {self.ride}"
