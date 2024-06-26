import logging

from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView

from apps.address_manager.models.city import City
from apps.address_manager.models.state import State
from apps.core.models.custom_user import CustomUser
from apps.core.utils.cpf_validator import CpfValidator
from apps.core.utils.regex_utils import get_only_numbers
from apps.ride_manager.forms import RegistrationForm
from apps.ride_manager.forms.form_person import PersonForm
from apps.ride_manager.services.code_validator_service import (
    CodeValidatorService,
)
from apps.ride_manager.services.person_register_service import (
    PersonRegisterService,
)
from apps.term_manager.enums.term_choices import TermTypeChoices
from apps.term_manager.models import Term


class RegistrationFormView(FormView):
    template_name = "register.html"
    form_class = RegistrationForm
    success_url = "home"

    def form_valid(self, form):
        super().form_valid(form)
        avatar = form.cleaned_data.get("avatar")
        document_picture = form.cleaned_data.get("document_picture")
        del form.cleaned_data["avatar"]
        del form.cleaned_data["document_picture"]

        service = PersonRegisterService(data=form.cleaned_data)
        with transaction.atomic():
            user = service.create_custom_user()
            person = service.create_person(user)

            if avatar:
                person.avatar = avatar

            if document_picture:
                person.document_picture = document_picture

            person.save()
            service.create_acceptance_terms(person)

        login(self.request, user)
        return redirect("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["states"] = State.objects.all()
        context["cities"] = City.objects.all()
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
        return context


def register(request):
    """
    The register consists os three steps, the first the person must validate
    the phone number, next create a user account and finally register the person
    """
    """
    TODO reactivate twillio integration
    if (
        "phone_validation" not in request.session
        or request.session["phone_validation"] is False
    ):
        return redirect("send_verify_code")
    """

    states = State.objects.all()
    cities = City.objects.all()
    if request.method == "POST":
        error = ""
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save(commit=False)

            cpf = get_only_numbers(request.POST.get("cpf"))
            cpf_validator = CpfValidator()
            if not cpf_validator.validate_cpf(cpf):
                print(f"\n\n\n\nCPF inválido.")
                error = "CPF inválido."
                return render(
                    request,
                    "register.html",
                    {"form": form, "states": states, "cities": cities},
                )

            if CustomUser.objects.filter(cpf=cpf).exists():
                error = "CPF já cadastrado."
                return render(
                    request,
                    "register.html",
                    {"form": form, "states": states, "cities": cities},
                )

            with transaction.atomic():
                user = create_user(request, form)
                print(f"\n\n\n\n{user=}")
                person.user = user
                person.save()

            login(request, user)
            return redirect("home")
        else:
            print(form.errors)
    else:
        form = PersonForm()
    return render(
        request,
        "register.html",
        {"form": form, "states": states, "cities": cities, "error": ""},
    )


def create_user(request, form):
    cpf = request.POST.get("cpf")
    password = request.POST.get("password")

    try:
        user = CustomUser.objects.create_user(
            cpf=cpf,
            password=password,
        )
        splitted_names = form.cleaned_data.get("name").split(" ")
        user.first_name = splitted_names[0].capitalize()
        user.last_name = splitted_names[-1].capitalize()

        user.save()
        return user
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        return e


def send_verify_code(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        validator_service = CodeValidatorService()
        response = validator_service.send_code(phone)
        request.session["phone"] = phone
        request.session["validation_service_sid"] = response.service_sid
        return redirect("validate_code")
    return render(request, "send_verify_code.html")


def validate_code(request):
    validation_service_sid = request.session.get("validation_service_sid")
    phone = request.session.get("phone")
    code = ""

    if request.method == "POST":
        for i in range(1, 7):
            code += request.POST.get(f"code{i}")

        validator_service = CodeValidatorService()
        if validator_service.is_code_valid(phone, code, validation_service_sid):
            request.session["phone_validation"] = True
            return redirect("register")
    return render(request, "validate_code.html")
