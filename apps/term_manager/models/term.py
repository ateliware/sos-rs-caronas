from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel
from apps.core.utils.choices_validator import validate_choice
from apps.term_manager.enums import TermTypeChoices


class Term(BaseModel):
    class Meta:
        verbose_name = "Termo"
        verbose_name_plural = "Termos"

    version = models.CharField(
        max_length=255,
        verbose_name="Versão",
    )
    type = models.CharField(
        max_length=255,
        choices=TermTypeChoices.choices,
        verbose_name="Tipo de termo",
    )
    content = models.TextField(
        verbose_name="Conteúdo",
    )

    def save(self, *args, **kwargs):
        is_valid_choice = validate_choice(self.type, TermTypeChoices)
        if not is_valid_choice:
            raise ValidationError(
                {
                    "type": f"Tipo de termo {self.type} inválido.",
                }
            )
        super().save(*args, **kwargs)

    def __str__(self):
        term_type = getattr(TermTypeChoices, self.type).label
        return f"{term_type} | {self.version}"
