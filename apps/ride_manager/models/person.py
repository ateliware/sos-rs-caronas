import os
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel, CustomUser
from apps.core.utils.cpf_validator import CpfValidator
from apps.core.utils.regex_utils import get_only_numbers
from apps.address_manager.models.base_address import BaseAddress

def upload_path(instance, filename):
    return os.path.join(
        "person_files",
        str(instance.uuid),
        filename,
    )

class Person(BaseModel):
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
    )
    emergency_contact = models.CharField(
        max_length=255,
        verbose_name="Contato de emergência",
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
        max_length=11,
        verbose_name="Número da CNH",
        unique=True,
        null=True,
        blank=True,
    )
    cnh_picture = models.ImageField(
        upload_to=upload_path,
        verbose_name="Imagem da CNH",
        null=True,
        blank=True,
    )
    cpf = models.CharField(
        max_length=11,
        verbose_name="CPF",
        unique=True,
    )
    document_picture = models.ImageField(
        upload_to=upload_path,
        verbose_name="Imagem do documento",
        null=True,
        blank=True,
    )
    is_verified = models.BooleanField(
        verbose_name="Verificado",
        default=False,
    )
    
    def save(self, *args, **kwargs):
        self.cpf = get_only_numbers(self.cpf)
        cpf_is_valid = CpfValidator().validate_cpf(self.cpf)

        if not cpf_is_valid:
            raise ValidationError({"cpf": "CPF inválido."})
        
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name