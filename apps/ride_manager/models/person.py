import os
from uuid import uuid4

from django.db import models

from apps.address_manager.models.base_address import BaseAddress
from apps.core.models import BaseModel, CustomUser


def upload_path(instance, filename):
    return os.path.join(
        "person_files",
        str(instance.uuid),
        filename,
    )


class Person(BaseModel, BaseAddress):
    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid4,
        primary_key=True,
        editable=False,
        unique=True,
    )
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name="Usuário",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Nome completo",
    )
    phone = models.CharField(
        max_length=16,
        verbose_name="Telefone",
    )
    emergency_phone = models.CharField(
        max_length=16,
        verbose_name="Telefone de emergência",
        null=True,
        blank=True,
    )
    emergency_contact = models.CharField(
        max_length=255,
        verbose_name="Contato de emergência",
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        verbose_name="Data de nascimento",
    )
    avatar = models.ImageField(
        upload_to=upload_path,
        verbose_name="Imagem de perfil",
        null=True,
        blank=True,
    )
    cnh_number = models.CharField(
        max_length=15,
        verbose_name="Número da CNH",
        null=True,
        blank=True,
    )
    cnh_picture = models.ImageField(
        upload_to=upload_path,
        verbose_name="Imagem da CNH",
        null=True,
        blank=True,
    )
    cnh_is_verified = models.BooleanField(
        verbose_name="CNH verificada",
        default=False,
    )
    document_picture = models.ImageField(
        upload_to=upload_path,
        verbose_name="Imagem do documento",
        null=True,
        blank=True,
    )
    document_is_verified = models.BooleanField(
        verbose_name="Documento verificado",
        default=False,
    )
    profile_is_verified = models.BooleanField(
        verbose_name="Perfil verificado",
        default=False,
    )

    def __str__(self):
        return self.name
