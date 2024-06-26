from uuid import uuid4

from django.db import models

from apps.address_manager.models.city import City
from apps.core.models.base_model import BaseModel
from apps.ride_manager.enums.ride_status_choices import (
    ShiftChoices,
    StatusChoices,
)
from apps.ride_manager.models.affected_place import AffectedPlace
from apps.ride_manager.models.person import Person
from apps.ride_manager.models.vehicle import Vehicle


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
    goal_of_the_ride = models.CharField(
        max_length=255,
        verbose_name="Objetivo da Carona",
        default="Limpeza",
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
    quantity_of_passengers = models.PositiveIntegerField(
        verbose_name="Vagas Disponíveis", default=4
    )
    notes = models.TextField(
        verbose_name="Observações",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=15,
        choices=StatusChoices.choices,
        verbose_name="Status",
        default=StatusChoices.UNDER_REVIEW,
    )
    whatsapp_group_link = models.URLField(
        verbose_name="Link do Grupo de WhatsApp",
        blank=True,
        null=True,
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

        # if the driver's CNH is verified and the vehicle is verified, the ride status is set to OPEN
        if self.driver.cnh_is_verified and self.vehicle.is_verified:
            self.status = StatusChoices.OPEN

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.origin} - {self.destination} - {self.date} - {self.work_shift}"
