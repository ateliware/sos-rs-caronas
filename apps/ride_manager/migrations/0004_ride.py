# Generated by Django 4.2.11 on 2024-05-08 19:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("address_manager", "0001_initial"),
        ("ride_manager", "0003_affectedplace"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ride",
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
                ("date", models.DateField(verbose_name="Data da Viagem")),
                (
                    "work_shift",
                    models.CharField(
                        choices=[("MORNING", "Manhã"), ("AFTERNOON", "Tarde")],
                        max_length=15,
                        verbose_name="Turno",
                    ),
                ),
                ("notes", models.TextField(verbose_name="Observações")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Open", "Aberta"),
                            ("IN_PROGRESS", "Em Andamento"),
                            ("FINISHED", "Concluída"),
                        ],
                        max_length=11,
                        verbose_name="Status",
                    ),
                ),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="ride_manager.affectedplace",
                        verbose_name="Destino da Viagem",
                    ),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="ride_manager.person",
                        verbose_name="Motorista",
                    ),
                ),
                (
                    "origin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="address_manager.city",
                        verbose_name="Cidade Origem",
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="ride_manager.vehicle",
                        verbose_name="Veículo",
                    ),
                ),
            ],
            options={
                "verbose_name": "Carona",
                "verbose_name_plural": "Caronas",
            },
        ),
    ]