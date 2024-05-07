import logging

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.core.serializers.standard_response_serializer import (
    StandardResponseSerializer,
)
from apps.core.utils.choices_validator import validate_choice
from apps.term_manager.enums.term_choices import TermTypeChoices
from apps.term_manager.models.term import Term
from apps.term_manager.serializers.term_serializers import TermSerializer


class TermViewSet(ViewSet):
    serializer_class = TermSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="type",
                description="tipo do termo",
                required=True,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            status.HTTP_200_OK: TermSerializer,
            status.HTTP_400_BAD_REQUEST: StandardResponseSerializer,
            status.HTTP_404_NOT_FOUND: StandardResponseSerializer,
            status.HTTP_500_INTERNAL_SERVER_ERROR: StandardResponseSerializer,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        term_type = request.query_params.get("type")
        response = {
            "message": "Tipo do termo é obrigatório",
        }
        if not term_type:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            term_type_is_valid = validate_choice(
                term_type.upper(), TermTypeChoices
            )
            if not term_type_is_valid:
                response = {
                    "message": "Tipo do termo inválido",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            term = (
                Term.objects.filter(
                    type=term_type.upper(),
                )
                .order_by("-created_at")
                .first()
            )

            if not term:
                response = {
                    "message": "Termo não encontrado",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            response = TermSerializer(term).data
            return Response(response)

        except Exception as err:
            logging.error(err)
            response = {
                "message": f"Erro ao buscar termo: {err}",
            }
            return Response(
                response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
