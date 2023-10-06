from django.urls import path

from core.views import (
    post_detail,
    PostListView,
    SignUpView,
    reply_view,
    PostCreateView,
    ProfileDetailView,
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("/signup/", SignUpView.as_view(), name="signup"),
    path("/profile/<int:pk>/", ProfileDetailView.as_view(), name="profile"),
    path("/comment/reply/", reply_view, name="reply"),
    path("<slug:post>/", post_detail, name="post_detail"),
    path("<slug:slug>/update/", PostUpdateView.as_view(), name="post_update"),
    path("<slug:slug>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("tag/<slug:tag_slug>/", PostListView.as_view(), name='post_tag'),
    path("user/<int:pk>/", PostListView.as_view(), name='post_user')
]

app_name = "core"
