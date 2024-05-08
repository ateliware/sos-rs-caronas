from uuid import uuid4

from django.db import models

from apps.address_manager.models.city import City
from apps.core.models.base_model import BaseModel


class AffectedPlace(BaseModel):
    class Meta:
        verbose_name = "Local Afetado"
        verbose_name_plural = "Locais Afetados"

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid4,
        primary_key=True,
        editable=False,
        unique=True,
    )
    description = models.CharField(
        verbose_name="Descrição",
        max_length=255,
    )
    informations = models.TextField(
        verbose_name="Informações Básicas",
    )
    address = models.TextField(
        verbose_name="Endereço de Chegada",
    )
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        verbose_name="Cidade",
    )
    main_person = models.CharField(
        max_length=255,
        verbose_name="Responsável(is)",
    )
    main_contact = models.CharField(
        max_length=255,
        verbose_name="Telefone(s) Principal(is)",
    )

    def __str__(self):
        return self.description
