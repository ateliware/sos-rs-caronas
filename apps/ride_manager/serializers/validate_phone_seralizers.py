from rest_framework import serializers


class ValidatePhoneSendCodeRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)


class ValidatePhoneSendCodeResponseOKSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    validation_uuid = serializers.CharField(required=True)


class ValidatePhoneCheckCodeRequestSerializer(serializers.Serializer):
    validation_uuid = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
