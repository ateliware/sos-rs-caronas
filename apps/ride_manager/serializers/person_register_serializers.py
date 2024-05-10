from datetime import date

from rest_framework import serializers

from apps.core.serializers.base_64_serializer import Base64FileField
from apps.core.utils.age_calculator import get_age
from apps.ride_manager.models.person import Person


class PersonRegisterSerializer(serializers.Serializer):
    cpf = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)
    name = serializers.CharField(max_length=255, required=True)
    phone = serializers.CharField(max_length=16, required=True)
    validation_uuid = serializers.CharField(required=True)
    emergency_phone = serializers.CharField(max_length=16, required=False)
    emergency_contact = serializers.CharField(max_length=255, required=False)
    birth_date = serializers.DateField(required=True)
    avatar = Base64FileField(default_filename="avatar.jpg", required=False)
    city_id = serializers.IntegerField(required=True)
    lgpd_acceptance = serializers.BooleanField(required=True)

    # method name must me validate_<field_name> to validate a specific field
    def validate_password_confirm(self, value):
        if value != self.initial_data["password"]:
            raise serializers.ValidationError("Senhas não conferem.")

        return value

    def validate_lgpd_acceptance(self, value):
        if not value:
            raise serializers.ValidationError(
                "Você deve aceitar os termos de uso para continuar."
            )

        return value


class PersonRegisterResponseSerializer(serializers.Serializer):
    person_uuid = serializers.CharField()


class PersonModelSerializer(serializers.ModelSerializer):
    avatar = Base64FileField(default_filename="avatar.jpg", required=False)
    cnh_picture = Base64FileField(
        default_filename="cnh_picture.jpg", required=False
    )
    document_picture = Base64FileField(
        default_filename="document_picture.jpg", required=False
    )

    class Meta:
        model = Person
        fields = [
            "uuid",
            "user",
            "name",
            "phone",
            "emergency_phone",
            "emergency_contact",
            "birth_date",
            "avatar",
            "cnh_number",
            "cnh_picture",
            "cnh_is_verified",
            "document_picture",
            "document_is_verified",
            "city",
            "zip_code",
        ]
        read_only_fields = [
            "uuid",
        ]
        write_only_fields = [
            "user",
        ]

    def to_representation(self, data):
        response_data = super().to_representation(data)
        response_data.pop("user", None)
        return response_data


class PersonSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            "uuid",
            "name",
            "phone",
            "city",
            "age",
        ]
        read_only_fields = [
            "uuid",
            "name",
            "phone",
            "city",
            "age",
        ]

    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        today = date.today()
        age = get_age(instance.birth_date, today)
        response_data["age"] = age
        return response_data
