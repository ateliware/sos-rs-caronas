import logging

from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.serializers import StandardResponseSerializer
from apps.ride_manager.models.phone_validation import PhoneValidation
from apps.ride_manager.serializers import (
    ValidatePhoneCheckCodeRequestSerializer,
)
from apps.ride_manager.services.code_validator_service import (
    CodeValidatorService,
)


class ValidatePhoneCheckCodeApiView(APIView):
    @extend_schema(
        request=ValidatePhoneCheckCodeRequestSerializer,
        responses={
            status.HTTP_200_OK: StandardResponseSerializer,
            status.HTTP_400_BAD_REQUEST: StandardResponseSerializer,
            status.HTTP_404_NOT_FOUND: StandardResponseSerializer,
            status.HTTP_500_INTERNAL_SERVER_ERROR: StandardResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = ValidatePhoneCheckCodeRequestSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {
                    "message": "Erro ao validar os dados.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validation_uuid = data.get("validation_uuid")
            phone = data.get("phone")
            code = data.get("code")

            phone_validation = get_object_or_404(
                PhoneValidation,
                uuid=validation_uuid,
                phone=phone,
            )

            validator = CodeValidatorService()
            if validator.is_code_valid(
                phone, code, phone_validation.integration_sid
            ):
                phone_validation.is_active = True
                phone_validation.save()

                return Response(
                    {"message": "Código validado com sucesso."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Código inválido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Http404:
            return Response(
                {"message": "UUID de validação não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as error:
            logging.error(
                f"Error when try validate code, with message: {error}"
            )
            return Response(
                {"message": "Erro ao tentar validar o código de verificação."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
