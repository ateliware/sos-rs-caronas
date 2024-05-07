from django.db import models

from apps.core.models import BaseModel


class State(BaseModel):
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    name = models.CharField(
        verbose_name="Nome",
        max_length=100,
    )
    code = models.CharField(
        verbose_name="Código",
        max_length=2,
    )

    def save(self, *args, **kwargs):
        # turn code in uppercase before save
        self.code = self.code.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
