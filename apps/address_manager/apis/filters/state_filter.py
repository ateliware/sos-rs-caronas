from django_filters import rest_framework as filters

from apps.address_manager.models.state import State


class StateFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
    )
    code = filters.CharFilter(
        field_name="code",
        lookup_expr="icontains",
    )

    class Meta:
        model = State
        fields = ["name", "code"]
