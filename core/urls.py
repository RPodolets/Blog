from django.urls import path

from core.views import post_detail, PostListView, SignUpView, reply_view

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("<slug:post>/", post_detail, name="post_detail"),
    path("/signup/", SignUpView.as_view(), name="signup"),
    path("/comment/reply/", reply_view, name="reply")
]

app_name = "core"
