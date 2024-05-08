# Generated by Django 4.2.11 on 2024-05-08 14:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("address_manager", "0001_initial"),
        ("ride_manager", "0002_vehicle"),
    ]

    operations = [
        migrations.CreateModel(
            name="AffectedPlace",
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
                    "description",
                    models.CharField(max_length=255, verbose_name="Descrição"),
                ),
                (
                    "informations",
                    models.TextField(verbose_name="Informações Básicas"),
                ),
                (
                    "address",
                    models.TextField(verbose_name="Endereço de Chegada"),
                ),
                (
                    "main_person",
                    models.CharField(
                        max_length=255, verbose_name="Responsável(is)"
                    ),
                ),
                (
                    "main_contact",
                    models.CharField(
                        max_length=255, verbose_name="Telefone(s) Principal(is)"
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="address_manager.city",
                        verbose_name="Cidade",
                    ),
                ),
            ],
            options={
                "verbose_name": "Local Afetado",
                "verbose_name_plural": "Locais Afetados",
            },
        ),
    ]