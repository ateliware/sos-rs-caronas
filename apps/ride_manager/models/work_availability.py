from django.db import models
from django.forms import ValidationError

from apps.address_manager.models.city import City
from apps.core.models import BaseModel
from apps.core.utils.choices_validator import validate_choice
from apps.ride_manager.enums import (
    WorkAvailabilityStatusChoices,
    WorkShiftChoices,
)
from apps.ride_manager.models.affected_place import AffectedPlace
from apps.ride_manager.models.person import Person


class WorkAvailability(BaseModel):
    class Meta:
        verbose_name = "Disponibilidade de trabalho"
        verbose_name_plural = "Disponibilidades de trabalho"

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name="Pessoa",
    )
    origin = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name="Cidade",
    )
    destination = models.ForeignKey(
        AffectedPlace,
        on_delete=models.CASCADE,
        verbose_name="Local afetado",
        null=True,
        blank=True,
    )
    any_destination = models.BooleanField(
        verbose_name="Qualquer destino?",
        default=False,
    )
    date = models.DateField(
        verbose_name="Data",
    )
    work_shift = models.CharField(
        max_length=255,
        verbose_name="Turno de trabalho",
        choices=WorkShiftChoices.choices,
        default=WorkShiftChoices.ALL_DAY,
    )
    status = models.CharField(
        max_length=255,
        verbose_name="Status",
        choices=WorkAvailabilityStatusChoices.choices,
        default=WorkAvailabilityStatusChoices.OPEN,
    )

    def save(self, *args, **kwargs):
        work_shift_is_valid = validate_choice(self.work_shift, WorkShiftChoices)
        if not work_shift_is_valid:
            raise ValidationError({"work_shift": "Turno de trabalho inválido"})
        status_is_valid = validate_choice(
            self.status, WorkAvailabilityStatusChoices
        )
        if not status_is_valid:
            raise ValidationError({"status": "Status inválido"})
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.person} - {self.city} - {self.affected_place}"
