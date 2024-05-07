from django.db import models

from apps.address_manager.models.base_address import BaseAddress
from apps.core.models import BaseModel, CustomUser


class Address(BaseModel, BaseAddress):
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    description = models.CharField(
        max_length=255,
        verbose_name="Descrição",
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Usuário",
    )

    def __str__(self):
        return str(self.id)
