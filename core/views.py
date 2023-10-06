from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from taggit.models import Tag

from core.forms import CommentForm, SignUpForm, PostForm, PostSearchForm
from core.models import Post, Comment, Profile


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    queryset = Post.published.prefetch_related("tags").select_related("author", "author__user")
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = PostSearchForm(
            initial={"title": title}
        )
        tag_list = Tag.objects.annotate(
            post_count=Count('taggit_taggeditem_items')
        ).order_by("-post_count")[:5]
        context["tag_list"] = tag_list
        return context

    def get_queryset(self, *args, **kwargs):
        if search := self.request.GET.get("title", ""):
            self.queryset = self.queryset.filter(title__icontains=search)

        if tag := self.kwargs.get("tag_slug", ""):
            print(tag)
            self.queryset = self.queryset.filter(tags__name__in=[tag])

        if pk := self.request.GET.get("pk", ""):
            self.queryset = self.queryset.filter(user__profile__id=pk)

        return self.queryset


@login_required(login_url='/accounts/login/')
def post_detail(request: HttpRequest, post: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=post, status='published')

    if post:
        post.update_views()

    comments = post.comments.filter(active=True)
    comment_form = CommentForm()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
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


@login_required(login_url='/accounts/login/')
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


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = "core/post_form.html"
    success_url = ""

    def form_valid(self, form):
        form.instance.author = Profile.objects.get(user__id=self.request.user.id)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = "core/post_form.html"
    success_url = ""


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile
