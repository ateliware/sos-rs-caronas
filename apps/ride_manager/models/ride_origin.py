from uuid import uuid4

from django.db import models

from apps.address_manager.models.city import City
from apps.core.models.base_model import BaseModel


class RideOrigin(BaseModel):
    class Meta:
        verbose_name = "Origem da Carona"
        verbose_name_plural = "Origens das Caronas"

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid4,
        primary_key=True,
        editable=False,
        unique=True,
    )
    city = models.OneToOneField(
        City,
        on_delete=models.PROTECT,
        verbose_name="Cidade",
    )
    enabled = models.BooleanField(
        verbose_name="Permitido?",
        default=True,
    )

    def __str__(self):
        return self.city.name
