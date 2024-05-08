import os
from uuid import uuid4
from django.db import models

from apps.core.models import BaseModel
from apps.ride_manager.models.person import Person


def upload_path(instance, filename):
    return os.path.join(
        "vehicle_files",
        str(instance.uuid),
        filename,
    )


class Vehicle(BaseModel):
    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veiculos"

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid4,
        primary_key=True,
        editable=False,
        unique=True,
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name="Pessoa",
    )
    model = models.CharField(
        max_length=255,
        verbose_name="Modelo do veículo",
    )
    color = models.CharField(
        max_length=255,
        verbose_name="Cor do veículo",
    )
    plate = models.CharField(
        max_length=9,
        verbose_name="Placa",
    )
    plate_picture = models.ImageField(
        upload_to=upload_path,
        verbose_name="Imagem da placa",
    )
    vehicle_picture = models.ImageField(
        upload_to=upload_path,
        verbose_name="Imagem da veículo",
    )
    is_verified = models.BooleanField(
        verbose_name="Verificado",
        default=False,
    )

    def __str__(self):
        return self.model
