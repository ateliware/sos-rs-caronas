from rest_framework import serializers

from apps.core.serializers.base_64_serializer import Base64FileField


class PersonRegisterSerializer(serializers.Serializer):
    cpf = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)    
    name = serializers.CharField(max_length=255, required=True)
    phone = serializers.CharField(max_length=16, required=True)
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