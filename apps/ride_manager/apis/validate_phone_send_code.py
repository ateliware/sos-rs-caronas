import logging

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.serializers import (
    StandardResponseSerializer,
    StandardResponseSerializerError,
)
from apps.ride_manager.models.phone_validation import PhoneValidation
from apps.ride_manager.serializers import (
    ValidatePhoneSendCodeRequestSerializer,
    ValidatePhoneSendCodeResponseOKSerializer,
)
from apps.ride_manager.services.code_validator_service import (
    CodeValidatorService,
)


class ValidatePhoneSendCodeApiView(APIView):
    @extend_schema(
        request=ValidatePhoneSendCodeRequestSerializer,
        responses={
            status.HTTP_200_OK: ValidatePhoneSendCodeResponseOKSerializer,
            status.HTTP_400_BAD_REQUEST: StandardResponseSerializerError,
            status.HTTP_500_INTERNAL_SERVER_ERROR: StandardResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = ValidatePhoneSendCodeRequestSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {
                    "message": "Erro ao validar os dados.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            phone = data.get("phone")
            validator = CodeValidatorService()

            verification = validator.send_code(data.get("phone"))
            phone_validation = PhoneValidation.objects.create(
                phone=phone,
                integration_sid=verification.service_sid,
            )
            return Response(
                {
                    "message": "Código Enviado.",
                    "validation_uuid": str(phone_validation.uuid),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            logging.error(f"Error when try send code, with message: {error}")
            return Response(
                {
                    "message": "Erro ao tentar enviar o código de verificação.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
