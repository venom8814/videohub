"""Представления приложения videos."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse

from .models import Video, VideoReaction, Comment, VideoView
from .forms import VideoUploadForm, CommentForm


# ──────────────────────────────────────────────────────────
# Главная страница
# ──────────────────────────────────────────────────────────
def home(request):
    """
    Главная страница: список видео.
    Поддерживает сортировку: newest (по умолчанию) и popular.
    """
    sort   = request.GET.get("sort", "newest")
    query  = request.GET.get("q", "").strip()

    videos = Video.objects.select_related("author").all()

    # Поиск по названию / описанию
    if query:
        videos = videos.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Сортировка
    if sort == "popular":
        videos = videos.order_by("-views")
    else:
        videos = videos.order_by("-upload_date")

    return render(request, "home.html", {
        "videos": videos,
        "sort":   sort,
        "query":  query,
    })


# ──────────────────────────────────────────────────────────
# Страница видео
# ──────────────────────────────────────────────────────────
def video_detail(request, pk):
    """Страница просмотра видео с плеером, лайками и комментариями."""
    video = get_object_or_404(Video, pk=pk)

    # Подсчёт уникальных просмотров по session_key
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    _, created = VideoView.objects.get_or_create(video=video, session_id=session_id)
    if created:
        video.views += 1
        video.save(update_fields=["views"])

    # Текущая реакция пользователя
    user_reaction = None
    if request.user.is_authenticated:
        try:
            user_reaction = VideoReaction.objects.get(video=video, user=request.user).reaction_type
        except VideoReaction.DoesNotExist:
            pass

    # Форма комментария
    comment_form = CommentForm()
    if request.method == "POST" and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment        = comment_form.save(commit=False)
            comment.video  = video
            comment.author = request.user
            comment.save()
            messages.success(request, "Комментарий добавлен.")
            return redirect("video_detail", pk=pk)

    comments = video.comments.select_related("author").all()

    return render(request, "videos/video_detail.html", {
        "video":         video,
        "comments":      comments,
        "comment_form":  comment_form,
        "user_reaction": user_reaction,
    })


# ──────────────────────────────────────────────────────────
# Загрузка видео
# ──────────────────────────────────────────────────────────
@login_required
def video_upload(request):
    """Форма загрузки нового видео."""
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video        = form.save(commit=False)
            video.author = request.user
            video.save()
            messages.success(request, "Видео успешно загружено.")
            return redirect("video_detail", pk=video.pk)
    else:
        form = VideoUploadForm()

    return render(request, "videos/video_upload.html", {"form": form})


# ──────────────────────────────────────────────────────────
# Удаление видео
# ──────────────────────────────────────────────────────────
@login_required
def video_delete(request, pk):
    """Удаление видео — только автором."""
    video = get_object_or_404(Video, pk=pk, author=request.user)
    if request.method == "POST":
        video.delete()
        messages.success(request, "Видео удалено.")
        return redirect("dashboard")
    return render(request, "videos/video_confirm_delete.html", {"video": video})


# ──────────────────────────────────────────────────────────
# Лайк / дизлайк (AJAX)
# ──────────────────────────────────────────────────────────
@login_required
def react_video(request, pk):
    """
    POST-запрос для переключения лайка/дизлайка.
    Принимает параметр reaction_type: like | dislike
    """
    if request.method != "POST":
        return JsonResponse({"error": "Метод не поддерживается."}, status=405)

    video         = get_object_or_404(Video, pk=pk)
    reaction_type = request.POST.get("reaction_type")

    if reaction_type not in ("like", "dislike"):
        return JsonResponse({"error": "Неверный тип реакции."}, status=400)

    existing = VideoReaction.objects.filter(video=video, user=request.user).first()

    if existing:
        if existing.reaction_type == reaction_type:
            # Повторное нажатие — снимаем реакцию
            existing.delete()
            current_reaction = None
        else:
            # Смена реакции
            existing.reaction_type = reaction_type
            existing.save()
            current_reaction = reaction_type
    else:
        VideoReaction.objects.create(video=video, user=request.user, reaction_type=reaction_type)
        current_reaction = reaction_type

    return JsonResponse({
        "likes":    video.likes_count,
        "dislikes": video.dislikes_count,
        "reaction": current_reaction,
    })


# ──────────────────────────────────────────────────────────
# Личный кабинет
# ──────────────────────────────────────────────────────────
@login_required
def dashboard(request):
    """Список видео текущего пользователя."""
    videos = Video.objects.filter(author=request.user).order_by("-upload_date")
    return render(request, "videos/dashboard.html", {"videos": videos})
