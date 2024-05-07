# Generated by Django 4.2.11 on 2024-05-07 21:50

import apps.ride_manager.models.person
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("address_manager", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Ativo"),
                ),
                (
                    "zip_code",
                    models.CharField(max_length=9, verbose_name="CEP"),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="Nome completo"
                    ),
                ),
                (
                    "phone",
                    models.CharField(max_length=16, verbose_name="Telefone"),
                ),
                (
                    "emergency_phone",
                    models.CharField(
                        max_length=16, verbose_name="Telefone de emergência"
                    ),
                ),
                (
                    "emergency_contact",
                    models.CharField(
                        max_length=255, verbose_name="Contato de emergência"
                    ),
                ),
                (
                    "birth_date",
                    models.DateField(verbose_name="Data de nascimento"),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=apps.ride_manager.models.person.upload_path,
                        verbose_name="Imagem de perfil",
                    ),
                ),
                (
                    "cnh_number",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        null=True,
                        verbose_name="Número da CNH",
                    ),
                ),
                (
                    "cnh_picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=apps.ride_manager.models.person.upload_path,
                        verbose_name="Imagem da CNH",
                    ),
                ),
                (
                    "cpf",
                    models.CharField(
                        max_length=11, unique=True, verbose_name="CPF"
                    ),
                ),
                (
                    "document_picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=apps.ride_manager.models.person.upload_path,
                        verbose_name="Imagem do documento",
                    ),
                ),
                (
                    "is_verified",
                    models.BooleanField(
                        default=False, verbose_name="Verificado"
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="address_manager.city",
                        verbose_name="Cidade",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Usuário",
                    ),
                ),
            ],
            options={
                "verbose_name": "Pessoa",
                "verbose_name_plural": "Pessoas",
            },
        ),
    ]
