from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Atualizado em",
        auto_now=True,
    )
    is_active = models.BooleanField(
        verbose_name="Ativo",
        default=True,
    )

    class Meta:
        abstract = True
