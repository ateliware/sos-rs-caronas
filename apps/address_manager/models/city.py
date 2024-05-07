from django.db import models

from apps.address_manager.models.state import State
from apps.core.models import BaseModel


class City(BaseModel):
    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"

    name = models.CharField(
        verbose_name="Nome",
        max_length=100,
    )
    state = models.ForeignKey(
        State,
        verbose_name="Estado",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name} | {self.state.code}"
