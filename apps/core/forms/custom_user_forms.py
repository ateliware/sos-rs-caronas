from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from apps.core.models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password_1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
    )
    password_2 = forms.CharField(
        label="Confirmação de senha", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ["email"]

    def clean_password_2(self):
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")
        if password_1 and password_2 and password_1 != password_2:
            raise ValidationError("Passwords don't match")
        return password_2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password_1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ["email", "password", "is_active", "is_staff"]
