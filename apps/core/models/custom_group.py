from django.contrib.auth.models import Group


class CustomGroup(Group):
    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"
        proxy = True
        app_label = "core"
