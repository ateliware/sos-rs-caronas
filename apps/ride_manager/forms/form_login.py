from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from apps.core.utils.cpf_validator import CpfValidator
from apps.core.utils.regex_utils import get_only_numbers


class CustomLoginForm(AuthenticationForm):
    cpf = forms.CharField(
        label="cpf",
        max_length=15,
        min_length=11,
        required=True,
    )
    username = forms.CharField(label="username", required=False)

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")

        if cpf:
            cleaned_cpf = get_only_numbers(cpf)
            return cleaned_cpf

        else:
            raise forms.ValidationError("CPF é obrigatório")

    def clean(self) -> dict:
        cpf = self.cleaned_data.get("cpf")
        password = self.cleaned_data.get("password")

        if not cpf or not password:
            raise forms.ValidationError("CPF e senha são obrigatórios")

        if cpf:
            cpf_is_valid = CpfValidator().validate_cpf(cpf)

            if not cpf_is_valid:
                self.add_error("cpf", "CPF inválido")
                raise forms.ValidationError("CPF inválido")

        self.user_cache = authenticate(
            self.request,
            cpf=cpf,
            password=password,
        )

        if self.user_cache is None:
            raise forms.ValidationError("CPF ou senha inválidos")

        return self.cleaned_data
