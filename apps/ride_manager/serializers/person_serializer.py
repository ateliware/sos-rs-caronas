from rest_framework import serializers

from apps.core.serializers.base_64_serializer import Base64FileField
from apps.ride_manager.models.person import Person


class PersonSerializer(serializers.ModelSerializer):

    avatar = Base64FileField(default_filename="plate_picture.jpg")

    class Meta:
        model = Person
        fields = [
            "uuid",
            "name",
            "phone",
            "avatar",
            "birth_date",
            "created_at",
        ]
