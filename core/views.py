from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from core.models import Post


class PostListView(generic.ListView):
    model = Post
    queryset = Post.published.all()
    paginate_by = 3


def post_detail(request: HttpRequest, post: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=post, status="published")
    return render(request, "core/post_detail.html", {"post": post})

# class PostDetailView(generic.DetailView):
#     model = Post

