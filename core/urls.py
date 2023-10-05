from django.urls import path

from core.views import (
    post_detail,
    PostListView,
    SignUpView,
    reply_view,
    PostCreateView,
    ProfileDetailView
)

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("/signup/", SignUpView.as_view(), name="signup"),
    path("/profile/<int:pk>/", ProfileDetailView.as_view(), name="profile"),
    path("/comment/reply/", reply_view, name="reply"),
    path("<slug:post>/", post_detail, name="post_detail"),
    path("tag/<slug:tag_slug>/", PostListView.as_view(), name='post_tag'),
    path("user/<int:pk>/", PostListView.as_view(), name='post_user')
]

app_name = "core"
