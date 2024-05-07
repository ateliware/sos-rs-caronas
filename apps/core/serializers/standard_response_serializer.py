from rest_framework import serializers


class StandardResponseSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)


class StandardResponseSerializerError(serializers.Serializer):
    message = serializers.CharField(required=True)
    errors = serializers.CharField(required=True)
