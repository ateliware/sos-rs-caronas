# Generated by Django 4.2.11 on 2024-05-17 13:51

import apps.ride_manager.models.vehicle
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ride_manager", "0012_ride_goal_of_the_ride"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicle",
            name="plate_picture",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=apps.ride_manager.models.vehicle.upload_path,
                verbose_name="Imagem da placa",
            ),
        ),
    ]