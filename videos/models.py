"""Модели приложения videos."""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Video(models.Model):
    """Модель загруженного видео."""

    title       = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    video_file  = models.FileField("Видеофайл", upload_to="videos/")
    thumbnail   = models.ImageField("Превью", upload_to="thumbnails/", blank=True, null=True)
    author      = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="videos", verbose_name="Автор"
    )
    upload_date = models.DateTimeField("Дата загрузки", auto_now_add=True)
    views       = models.PositiveIntegerField("Просмотры", default=0)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ["-upload_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("video_detail", kwargs={"pk": self.pk})

    @property
    def likes_count(self):
        return self.reactions.filter(reaction_type="like").count()

    @property
    def dislikes_count(self):
        return self.reactions.filter(reaction_type="dislike").count()


class VideoReaction(models.Model):
    """Лайк / дизлайк от пользователя на видео."""

    REACTION_CHOICES = [
        ("like",    "Лайк"),
        ("dislike", "Дизлайк"),
    ]

    video         = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="reactions")
    user          = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="reactions")
    reaction_type = models.CharField("Тип реакции", max_length=10, choices=REACTION_CHOICES)

    class Meta:
        # Один пользователь — одна реакция на одно видео
        unique_together = ("video", "user")
        verbose_name = "Реакция"
        verbose_name_plural = "Реакции"

    def __str__(self):
        return f"{self.user.username} — {self.reaction_type} — {self.video.title}"


class Comment(models.Model):
    """Комментарий под видео."""

    video      = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="comments")
    author     = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="comments")
    text       = models.TextField("Текст")
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author.username}: {self.text[:40]}"


class VideoView(models.Model):
    """Уникальный просмотр видео (один сеанс — один счёт)."""

    video      = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="unique_views")
    session_id = models.CharField(max_length=40)
    viewed_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("video", "session_id")
