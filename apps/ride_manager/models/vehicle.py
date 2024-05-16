import os
from datetime import date
from uuid import uuid4

from django.apps import apps
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from apps.core.models import BaseModel
from apps.ride_manager.enums.ride_status_choices import (
    StatusChoices as RideStatusChoices,
)
from apps.ride_manager.models.person import Person


def upload_path(instance, filename):
    return os.path.join(
        "vehicle_files",
        str(instance.uuid),
        filename,
    )


class Vehicle(BaseModel):
    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veiculos"

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid4,
        primary_key=True,
        editable=False,
        unique=True,
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name="Pessoa",
    )
    model = models.CharField(
        max_length=255,
        verbose_name="Modelo do veículo",
    )
    color = models.CharField(
        max_length=255,
        verbose_name="Cor do veículo",
    )
    plate = models.CharField(
        max_length=9,
        verbose_name="Placa",
    )
    plate_picture = models.ImageField(
        upload_to=upload_path,
        verbose_name="Imagem da placa",
    )
    vehicle_picture = models.ImageField(
        upload_to=upload_path,
        verbose_name="Imagem da veículo",
    )
    is_verified = models.BooleanField(
        verbose_name="Verificado",
        default=False,
    )

    def __str__(self):
        return self.model


@receiver(post_delete, sender=Vehicle)
def delete_pictures(sender, instance, **kwargs):
    instance.plate_picture.delete(save=False)
    instance.vehicle_picture.delete(save=False)


@receiver(pre_save, sender=Vehicle)
def update_pictures(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Vehicle.objects.filter(pk=instance.pk).first()
        if (
            old_instance
            and old_instance.plate_picture != instance.plate_picture
        ):
            old_instance.plate_picture.delete(save=False)

        if (
            old_instance
            and old_instance.vehicle_picture != instance.vehicle_picture
        ):
            old_instance.vehicle_picture.delete(save=False)


@receiver(post_save, sender=Vehicle)
def update_under_review_rides(sender, instance, **kwargs):
    is_verified = instance.is_verified and instance.person.cnh_is_verified
    if is_verified:
        today = date.today()
        ride_model = apps.get_model("ride_manager", "Ride")
        rides = ride_model.objects.filter(
            vehicle=instance,
            status=RideStatusChoices.UNDER_REVIEW,
            date__gte=today,
        )
        if rides:
            rides.update(status=RideStatusChoices.OPEN)
