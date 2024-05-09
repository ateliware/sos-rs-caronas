from django.db import models
from django.forms import ValidationError

from apps.core.models import BaseModel
from apps.core.utils.choices_validator import validate_choice
from apps.ride_manager.enums import InviteStatusChoices
from apps.ride_manager.models.ride import Ride
from apps.ride_manager.models.voluntary import Voluntary


class Invite(BaseModel):
    class Meta:
        verbose_name = "Convite"
        verbose_name_plural = "Convites"

    ride = models.ForeignKey(
        Ride,
        on_delete=models.PROTECT,
        verbose_name="Carona",
    )
    voluntary = models.ForeignKey(
        Voluntary,
        on_delete=models.PROTECT,
        verbose_name="Voluntário",
    )
    status = models.CharField(
        max_length=255,
        verbose_name="Status",
        choices=InviteStatusChoices.choices,
        default=InviteStatusChoices.PENDING,
    )

    def save(self, *args, **kwargs):
        status_is_valid = validate_choice(self.status, InviteStatusChoices)
        if not status_is_valid:
            raise ValidationError({"status": "Status de convite inválido"})

        super().save(*args, **kwargs)
