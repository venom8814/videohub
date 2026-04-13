"""Формы приложения users."""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile


class RegisterForm(UserCreationForm):
    """Форма регистрации нового пользователя."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-input", "placeholder": "Email"}),
        label="Email",
    )

    class Meta:
        model  = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-input")


class LoginForm(AuthenticationForm):
    """Форма входа."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-input"


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля."""

    class Meta:
        model  = Profile
        fields = ["avatar", "bio"]
        widgets = {
            "bio":    forms.Textarea(attrs={"class": "form-textarea", "rows": 4}),
            "avatar": forms.FileInput(attrs={"class": "form-file"}),
        }
        labels = {
            "avatar": "Аватар",
            "bio":    "О себе",
        }
