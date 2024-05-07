from rest_framework import serializers

from apps.core.models.custom_user import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "email",
        ]
        read_only_fields = [
            "email",
        ]
