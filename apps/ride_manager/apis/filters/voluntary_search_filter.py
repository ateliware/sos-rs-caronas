from django_filters import rest_framework as filters

from apps.ride_manager.models.voluntary import Voluntary


class VoluntarySearchFilter(filters.FilterSet):
    class Meta:
        model = Voluntary
        fields = [
            "origin",
            "destination",
            "any_destination",
            "date",
            "work_shift",
        ]
