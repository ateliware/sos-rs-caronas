from uuid import uuid4

from django.db import models

from apps.address_manager.models.city import City
from apps.core.models.base_model import BaseModel
from apps.ride_manager.models.affected_place import AffectedPlace
from apps.ride_manager.models.person import Person
from apps.ride_manager.models.vehicle import Vehicle


class ShiftChoices(models.TextChoices):
    MORNING = "MORNING", "Manhã"
    AFTERNOON = "AFTERNOON", "Tarde"


class StatusChoices(models.TextChoices):
    OPEN = "Open", "Aberta"
    IN_PROGRESS = "IN_PROGRESS", "Em Andamento"
    FINISHED = "FINISHED", "Concluída"


class Ride(BaseModel):
    class Meta:
        verbose_name = "Carona"
        verbose_name_plural = "Caronas"

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid4,
        primary_key=True,
        editable=False,
        unique=True,
    )
    date = models.DateField(
        verbose_name="Data da Viagem",
    )
    work_shift = models.CharField(
        max_length=15,
        choices=ShiftChoices.choices,
        verbose_name="Turno",
    )
    origin = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        verbose_name="Cidade Origem",
    )
    destination = models.ForeignKey(
        AffectedPlace,
        on_delete=models.PROTECT,
        verbose_name="Destino da Viagem",
    )
    driver = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name="Motorista",
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        verbose_name="Veículo",
    )
    notes = models.TextField(
        verbose_name="Observações",
    )
    status = models.CharField(
        max_length=11,
        choices=StatusChoices.choices,
        verbose_name="Status",
    )

    def save(self, *args, **kwargs):
        is_shift_choice_valid = (
            self.work_shift in dict(ShiftChoices.choices).keys()
        )
        is_status_choice_valid = (
            self.status in dict(StatusChoices.choices).keys()
        )

        if not is_shift_choice_valid:
            raise ValueError("Turno inválido")
        if not is_status_choice_valid:
            raise ValueError("Status inválido")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.origin} - {self.destination} - {self.date} - {self.work_shift}"
