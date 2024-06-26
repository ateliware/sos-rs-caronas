# Generated by Django 4.2.11 on 2024-05-11 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "ride_manager",
            "0009_ride_quantity_of_passengers_ride_whatsapp_group_link_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="ride",
            name="status",
            field=models.CharField(
                choices=[
                    ("OPEN", "Aberta"),
                    ("IN_PROGRESS", "Em Andamento"),
                    ("FINISHED", "Concluída"),
                ],
                default="OPEN",
                max_length=11,
                verbose_name="Status",
            ),
        ),
    ]
