# Generated by Django 4.2.11 on 2024-05-10 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ride_manager", "0008_phonevalidation"),
    ]

    operations = [
        migrations.AddField(
            model_name="ride",
            name="quantity_of_passengers",
            field=models.PositiveIntegerField(
                default=4, verbose_name="Vagas Disponíveis"
            ),
        ),
        migrations.AddField(
            model_name="ride",
            name="whatsapp_group_link",
            field=models.URLField(
                blank=True, null=True, verbose_name="Link do Grupo de WhatsApp"
            ),
        ),
        migrations.AlterField(
            model_name="ride",
            name="notes",
            field=models.TextField(
                blank=True, null=True, verbose_name="Observações"
            ),
        ),
        migrations.AlterField(
            model_name="ride",
            name="status",
            field=models.CharField(
                choices=[
                    ("OPEN", "Aberta"),
                    ("IN_PROGRESS", "Em Andamento"),
                    ("FINISHED", "Concluída"),
                ],
                max_length=11,
                verbose_name="Status",
            ),
        ),
    ]