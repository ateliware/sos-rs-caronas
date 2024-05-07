from hashlib import sha256

from django.db import models

from apps.core.models import CustomUser
from apps.core.models.base_model import BaseModel
from apps.term_manager.models.term import Term


class TermAcceptance(BaseModel):
    class Meta:
        verbose_name = "Aceite de Termo"
        verbose_name_plural = "Aceites de Termo"

    term = models.ForeignKey(
        Term,
        on_delete=models.PROTECT,
        verbose_name="Termo",
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name="Usuário",
    )
    hashed_term = models.TextField(
        verbose_name="Hash do termo",
    )

    def save(self, *args, **kwargs):
        combined_content = f"{self.term.content}|{self.user.email}"
        self.hashed_term = sha256(combined_content.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} | {self.term}"
