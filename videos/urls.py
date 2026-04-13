from django.urls import path
from . import views

urlpatterns = [
    path("",                        views.home,          name="home"),
    path("upload/",                 views.video_upload,  name="video_upload"),
    path("dashboard/",              views.dashboard,     name="dashboard"),
    path("video/<int:pk>/",         views.video_detail,  name="video_detail"),
    path("video/<int:pk>/delete/",  views.video_delete,  name="video_delete"),
    path("video/<int:pk>/react/",   views.react_video,   name="react_video"),
]
