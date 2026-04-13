from django.contrib import admin
from .models import Video, VideoReaction, Comment, VideoView

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display  = ("title", "author", "upload_date", "views")
    search_fields = ("title", "author__username")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ("author", "video", "created_at")
    search_fields = ("author__username", "text")

admin.site.register(VideoReaction)
admin.site.register(VideoView)
