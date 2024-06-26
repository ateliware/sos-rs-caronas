# Generated by Django 4.2.11 on 2024-05-20 14:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("address_manager", "0001_initial"),
        ("ride_manager", "0013_alter_vehicle_plate_picture"),
    ]

    operations = [
        migrations.CreateModel(
            name="RideOrigin",
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
                    "enabled",
                    models.BooleanField(
                        default=True, verbose_name="Permitido?"
                    ),
                ),
                (
                    "city",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="address_manager.city",
                        verbose_name="Cidade",
                    ),
                ),
            ],
            options={
                "verbose_name": "Origem da Carona",
                "verbose_name_plural": "Origens das Caronas",
            },
        ),
    ]
