from uuid import uuid4

from django.db import models

from apps.core.models import BaseModel


class PhoneValidation(BaseModel):

    class Meta:
        verbose_name = "Validação de telefone"
        verbose_name_plural = "Validações de telefone"

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid4,
        primary_key=True,
        editable=False,
        unique=True,
    )
    integration_sid = models.CharField(
        max_length=36,
        verbose_name="Sid da Integração",
        editable=False,
        unique=True,
    )
    phone = models.CharField(
        max_length=16,
        verbose_name="Telefone",
    )
    is_active = models.BooleanField(
        verbose_name="Ativo",
        default=False,
    )

    def __str__(self):
        return str(self.uuid)
