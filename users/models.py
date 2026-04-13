"""Модели приложения users."""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Профиль пользователя — расширение стандартной модели User."""

    user   = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True, null=True)
    bio    = models.TextField("О себе", blank=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль {self.user.username}"
