from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from core.forms import CommentForm, SignUpForm
from core.models import Post, Comment, Profile


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    queryset = Post.published.all()
    paginate_by = 3


@login_required(login_url='/accounts/login/')
def post_detail(request: HttpRequest, post: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=post, status='published')

    comments = post.comments.filter(active=True)
    comment_form = CommentForm()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # new_comment.user = get_user_model().objects.get(id=request.user.id)
            new_comment.user = Profile.objects.get(user__id=request.user.id)
            new_comment.post = post
            new_comment.save()
            return redirect(post.get_absolute_url() + '#' + str(new_comment.id))

    return render(
        request,
        'core/post_detail.html',
        {
            'post': post,
            'comments': comments,
            "new_comment": new_comment,
            'comment_form': comment_form
        }
    )


def reply_view(request):
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = request.POST.get('post_id')
            parent_id = request.POST.get('parent')
            post_url = request.POST.get('post_url')
            reply = form.save(commit=False)

            reply.user = Profile.objects.get(user__id=request.user.id)
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            return redirect(post_url + '#' + str(reply.id))

    return redirect("/")


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
