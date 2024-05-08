from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from apps.core.models.custom_user import CustomUser
from apps.core.utils.cpf_validator import CpfValidator


class CustomUserCreationForm(forms.ModelForm):
    password_1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
    )
    password_2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = CustomUser
        fields = [
            "cpf",
            "first_name",
            "last_name",
            "email",
            "is_staff",
        ]

    def clean_password_2(self):
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")

        if password_1 and password_2 and password_1 != password_2:
            raise forms.ValidationError("Passwords don't match")

        return password_2

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        return validate_cpf(cpf)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password_1"])

        if commit:
            user.save()

        return user


class CustomUserChangeForm(forms.ModelForm):
    # Form for updating users, with hashed password
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = [
            "cpf",
            "first_name",
            "last_name",
            "email",
            "is_staff",
        ]

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        return validate_cpf(cpf)


def validate_cpf(cpf: str) -> str:
    validator = CpfValidator()
    cpf_is_valid = validator.validate_cpf(cpf)

    if not cpf_is_valid:
        raise forms.ValidationError("CPF digitado é inválido")

    return cpf
