from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.managers import CustomUserManager


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    email = models.EmailField(
        verbose_name="E-mail",
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name="Nome de usuário",
        max_length=255,
        null=True,
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # This is the field that will be used to login
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name
