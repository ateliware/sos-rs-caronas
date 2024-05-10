from django_filters import rest_framework as filters

from apps.ride_manager.models.ride import Ride


class RideFilter(filters.FilterSet):
    class Meta:
        model = Ride
        fields = [
            "origin",
            "destination",
            "date",
            "work_shift",
            "status",
        ]