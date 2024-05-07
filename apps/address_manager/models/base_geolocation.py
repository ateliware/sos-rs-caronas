from django.db import models


class BaseGeolocation(models.Model):
    """
    This class is an abstract model that defines the most common fields for a geolocation.
    This model can be inherited by other models that need to store geolocation information.
    """

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Latitude",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Longitude",
    )
    radius = models.IntegerField(
        verbose_name="Raio de atuação",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        # Truncate latitude and longitude to 6 decimal places
        self.latitude = round(float(self.latitude), 6)
        self.longitude = round(float(self.longitude), 6)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
