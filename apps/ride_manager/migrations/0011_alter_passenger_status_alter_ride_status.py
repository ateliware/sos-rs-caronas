# Generated by Django 4.2.11 on 2024-05-16 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ride_manager", "0010_alter_ride_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="passenger",
            name="status",
            field=models.CharField(
                choices=[
                    ("ACCEPTED", "Aceito"),
                    ("DECLINED", "Recusado"),
                    ("PENDING", "Pendente"),
                ],
                max_length=255,
                verbose_name="Status",
            ),
        ),
        migrations.AlterField(
            model_name="ride",
            name="status",
            field=models.CharField(
                choices=[
                    ("OPEN", "Aberta"),
                    ("UNDER_REVIEW", "Em análise"),
                    ("CROWDED", "Lotada"),
                    ("FINISHED", "Concluída"),
                ],
                default="UNDER_REVIEW",
                max_length=15,
                verbose_name="Status",
            ),
        ),
    ]
