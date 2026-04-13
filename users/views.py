"""Представления приложения users."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegisterForm, LoginForm, ProfileEditForm
from .models import Profile
from videos.models import Video


# ──────────────────────────────────────────────────────────
# Регистрация
# ──────────────────────────────────────────────────────────
def register_view(request):
    """Регистрация нового пользователя."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаём пустой профиль автоматически
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


# ──────────────────────────────────────────────────────────
# Вход
# ──────────────────────────────────────────────────────────
def login_view(request):
    """Вход в систему."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Вы вошли как {user.username}.")
            return redirect(request.GET.get("next", "home"))
    else:
        form = LoginForm(request)

    return render(request, "users/login.html", {"form": form})


# ──────────────────────────────────────────────────────────
# Выход
# ──────────────────────────────────────────────────────────
@login_required
def logout_view(request):
    """Выход из системы."""
    if request.method == "POST":
        logout(request)
        messages.info(request, "Вы вышли из системы.")
    return redirect("home")


# ──────────────────────────────────────────────────────────
# Профиль пользователя
# ──────────────────────────────────────────────────────────
def profile_view(request, username):
    """Публичная страница профиля."""
    user   = get_object_or_404(User, username=username)
    # Убеждаемся, что профиль существует
    profile, _ = Profile.objects.get_or_create(user=user)
    videos = Video.objects.filter(author=user).order_by("-upload_date")

    return render(request, "users/profile.html", {
        "profile_user": user,
        "profile":      profile,
        "videos":       videos,
    })


# ──────────────────────────────────────────────────────────
# Редактирование профиля
# ──────────────────────────────────────────────────────────
@login_required
def profile_edit(request):
    """Редактирование собственного профиля."""
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён.")
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, "users/profile_edit.html", {"form": form})
