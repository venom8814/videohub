from django import forms
from .models import Video, Comment


class VideoUploadForm(forms.ModelForm):

    class Meta:
        model  = Video
        fields = ["title", "description", "video_file", "thumbnail"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Введите название видео",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-textarea",
                "rows": 4,
                "placeholder": "Описание видео (необязательно)",
            }),
            "video_file": forms.FileInput(attrs={"class": "form-file"}),
            "thumbnail":  forms.FileInput(attrs={"class": "form-file"}),
        }
        labels = {
            "title":       "Название",
            "description": "Описание",
            "video_file":  "Видеофайл",
            "thumbnail":   "Превью (необязательно)",
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model  = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={
                "class": "form-textarea",
                "rows": 3,
                "placeholder": "Написать комментарий...",
            }),
        }
        labels = {"text": ""}
