import os
from datetime import date
from uuid import uuid4

from django.apps import apps
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from apps.address_manager.models.base_address import BaseAddress
from apps.core.models import BaseModel, CustomUser
from apps.ride_manager.enums.ride_status_choices import (
    StatusChoices as RideStatusChoices,
)


def upload_path(instance, filename):
    return os.path.join(
        "person_files",
        str(instance.uuid),
        filename,
    )


class Person(BaseModel, BaseAddress):
    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid4,
        primary_key=True,
        editable=False,
        unique=True,
    )
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name="Usuário",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Nome completo",
    )
    phone = models.CharField(
        max_length=16,
        verbose_name="Telefone",
    )
    emergency_phone = models.CharField(
        max_length=16,
        verbose_name="Telefone de emergência",
        null=True,
        blank=True,
    )
    emergency_contact = models.CharField(
        max_length=255,
        verbose_name="Contato de emergência",
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        verbose_name="Data de nascimento",
    )
    avatar = models.ImageField(
        upload_to=upload_path,
        verbose_name="Imagem de perfil",
        null=True,
        blank=True,
    )
    cnh_number = models.CharField(
        max_length=15,
        verbose_name="Número da CNH",
        null=True,
        blank=True,
    )
    cnh_picture = models.ImageField(
        upload_to=upload_path,
        verbose_name="Imagem da CNH",
        null=True,
        blank=True,
    )
    cnh_is_verified = models.BooleanField(
        verbose_name="CNH verificada",
        default=False,
    )
    document_picture = models.ImageField(
        upload_to=upload_path,
        verbose_name="Imagem do documento",
        null=True,
        blank=True,
    )
    document_is_verified = models.BooleanField(
        verbose_name="Documento verificado",
        default=False,
    )
    profile_is_verified = models.BooleanField(
        verbose_name="Perfil verificado",
        default=False,
    )

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Person)
def delete_pictures(sender, instance, **kwargs):
    instance.avatar.delete(save=False)
    instance.cnh_picture.delete(save=False)
    instance.document_picture.delete(save=False)


@receiver(pre_save, sender=Person)
def update_pictures(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Person.objects.filter(pk=instance.pk).first()
        if old_instance and old_instance.avatar != instance.avatar:
            old_instance.avatar.delete(save=False)

        if old_instance and old_instance.cnh_picture != instance.cnh_picture:
            old_instance.cnh_picture.delete(save=False)

        if (
            old_instance
            and old_instance.document_picture != instance.document_picture
        ):
            old_instance.document_picture.delete(save=False)


@receiver(post_save, sender=Person)
def update_under_review_rides(sender, instance, **kwargs):
    if not instance.cnh_is_verified:
        return

    vehicle_model = apps.get_model("ride_manager", "Vehicle")
    vehicles = vehicle_model.objects.filter(
        person=instance,
        is_verified=True,
    )

    if not vehicles:
        return

    for vehicle in vehicles:
        today = date.today()
        ride_model = apps.get_model("ride_manager", "Ride")
        rides = ride_model.objects.filter(
            vehicle=vehicle,
            driver=instance,
            status=RideStatusChoices.UNDER_REVIEW,
            date__gte=today,
        )
        if rides:
            rides.update(status=RideStatusChoices.OPEN)
