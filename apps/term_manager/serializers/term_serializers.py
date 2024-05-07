from rest_framework import serializers

from apps.term_manager.models import Term


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = [
            "id",
            "version",
            "type",
            "content",
            "created_at",
        ]
