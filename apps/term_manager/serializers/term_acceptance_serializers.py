from rest_framework import serializers

from apps.term_manager.models import TermAcceptance


class TermAcceptanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermAcceptance
        fields = [
            "id",
            "term",
            "hashed_term",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "hashed_term",
            "created_at",
        ]
