from django.shortcuts import render

from apps.term_manager.enums.term_choices import TermTypeChoices
from apps.term_manager.models.term import Term


def about(request):
    context = {}
    context["privacy_policy"] = (
        Term.objects.filter(type=TermTypeChoices.PRIVACY)
        .order_by("-created_at")
        .first()
    )
    context["term_of_use"] = (
        Term.objects.filter(type=TermTypeChoices.USE)
        .order_by("-created_at")
        .first()
    )
    return render(request, "about.html", context)
