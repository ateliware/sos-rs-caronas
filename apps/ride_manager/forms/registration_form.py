from datetime import date, timedelta

from django import forms

from apps.core.models import CustomUser
from apps.core.utils.cpf_validator import CpfValidator
from apps.core.utils.regex_utils import get_only_numbers


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(min_length=9, max_length=15)
    cpf = forms.CharField(min_length=11, max_length=15, required=True)
    birth_date = forms.DateField(required=True)
    state_id = forms.IntegerField(required=True)
    city_id = forms.IntegerField(required=True)
    emergency_phone = forms.CharField(max_length=15, required=True)
    emergency_contact = forms.CharField(max_length=255, required=True)
    document_picture = forms.ImageField(required=True)
    password = forms.CharField(max_length=100, required=True)
    password_confirmation = forms.CharField(max_length=100, required=True)
    lgpd_acceptance = forms.BooleanField(required=True)

    field_labels = {
        "name": ("Nome Completo", "Insira seu nome completo"),
        "phone": ("Telefone/WhatsApp", "(11) 99999-9999"),
        "cpf": ("CPF", "999.999.999-99"),
        "birth_date": ("Data de Nascimento", ""),
        "state_id": ("Estado", ""),
        "city_id": ("Cidade", ""),
        "emergency_phone": ("Telefone de Emergência", "(11) 99999-9999"),
        "emergency_contact": (
            "Contato de Emergência",
            "Nome do contato de emergência",
        ),
        "document_picture": ("Foto do Documento", ""),
        "password": ("Senha", ""),
        "password_confirmation": ("Confirmação de Senha", ""),
        "lgpd_acceptance": ("Aceite dos Termos de Uso", ""),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, (label, placeholder) in self.field_labels.items():
            self.fields[field_name].label = label
            self.fields[field_name].widget.attrs["placeholder"] = placeholder

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")

        if not cpf:
            raise forms.ValidationError("CPF é obrigatório")

        cpf = get_only_numbers(cpf)
        cpf_is_valid = CpfValidator().validate_cpf(cpf)

        if not cpf_is_valid:
            raise forms.ValidationError("CPF inválido")

        if CustomUser.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("CPF já cadastrado")

        return cpf

    def clean_password_confirmation(self):
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")

        if password != password_confirmation:
            raise forms.ValidationError("Senhas não conferem")

        return password_confirmation

    def clean_lgpd_acceptance(self):
        lgpd_acceptance = self.cleaned_data.get("lgpd_acceptance")

        if not lgpd_acceptance:
            raise forms.ValidationError(
                "Você deve aceitar os termos de uso para continuar"
            )

        return lgpd_acceptance

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        today = date.today()
        min_birth_date = today - timedelta(days=365 * 18)

        if birth_date > min_birth_date:
            raise forms.ValidationError(
                "Você deve ter mais de 18 anos para se cadastrar"
            )

        return birth_date

    def clean_document_picture(self):
        document_picture = self.cleaned_data.get("document_picture")

        if not document_picture:
            raise forms.ValidationError("Foto do documento é obrigatória")

        return document_picture
