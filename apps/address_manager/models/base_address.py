from django.core.exceptions import ValidationError
from django.db import models

from apps.address_manager.models.city import City
from apps.address_manager.utils.zip_code_format_validator import (
    zip_code_format_validator,
)


class BaseAddress(models.Model):
    """
    This class is an abstract model that defines the most commom fields for an address.
    This model can be inherited by other models that need to store address information. Also, it
    can be combinated with BaseGeolocation model to store geolocation information.
    """

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name="Cidade",
    )
    zip_code = models.CharField(
        max_length=9,
        verbose_name="CEP",
    )

    def save(self, *args, **kwargs):
        zip_code_is_valid = zip_code_format_validator(self.zip_code)

        if not zip_code_is_valid:
            raise ValidationError({"zip_code": "CEP inválido."})

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
