from django.contrib import admin
from django.urls import path, include

from core.views import post_detail, PostListView

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("<slug:post>/", post_detail, name="post_detail"),
]

app_name = "core"
