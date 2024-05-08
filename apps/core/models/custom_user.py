from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.managers import CustomUserManager
from apps.core.utils.cpf_validator import CpfValidator
from apps.core.utils.regex_utils import get_only_numbers


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    cpf = models.CharField(
        max_length=11,
        verbose_name="CPF",
        unique=True,
    )
    email = models.EmailField(
        verbose_name="E-mail",
        max_length=255,
        null=True,
        blank=True,
    )
    username = models.CharField(
        verbose_name="Nome de usuário",
        max_length=255,
        null=True,
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "cpf"  # This is the field that will be used to login
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.cpf = get_only_numbers(self.cpf)
        cpf_is_valid = CpfValidator().validate_cpf(self.cpf)

        if not cpf_is_valid:
            raise ValidationError({"cpf": "CPF inválido."})

        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name
