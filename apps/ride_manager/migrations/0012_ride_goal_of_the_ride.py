# Generated by Django 4.2.11 on 2024-05-16 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ride_manager", "0011_alter_passenger_status_alter_ride_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="ride",
            name="goal_of_the_ride",
            field=models.CharField(
                default="Limpeza",
                max_length=255,
                verbose_name="Objetivo da Carona",
            ),
        ),
    ]
