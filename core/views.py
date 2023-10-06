from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from taggit.models import Tag

from core.forms import CommentForm, SignUpForm, PostForm, PostSearchForm, ProfileForm
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
            post_count=Count("taggit_taggeditem_items")
        ).order_by("-post_count")[:5]
        context["tag_list"] = tag_list
        return context

    def get_queryset(self, *args, **kwargs):
        if pk := self.kwargs.get("pk", ""):
            self.queryset = Post.objects.filter(
                author__id=pk).prefetch_related(
                "tags").select_related(
                "author", "author__user"
            )

        if search := self.request.GET.get("title", ""):
            self.queryset = self.queryset.filter(title__icontains=search)

        if tag := self.kwargs.get("tag_slug", ""):
            self.queryset = self.queryset.filter(tags__name__in=[tag])

        return self.queryset


@login_required(login_url="/accounts/login/")
def post_detail(request: HttpRequest, post: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=post)

    if post.status == "draft" and post.author.id != request.user.profile.id:
        raise Http404("Article not exists")

    if post:
        post.update_views()

    comments = post.comments.filter(active=True)
    comment_form = CommentForm()
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = Profile.objects.get(user__id=request.user.id)
            new_comment.post = post
            new_comment.save()
            return redirect(post.get_absolute_url() + "#" + str(new_comment.id))

    return render(
        request,
        "core/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form
        }
    )


@login_required(login_url="/accounts/login/")
def reply_view(request):
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = request.POST.get("post_id")
            post_url = request.POST.get("post_url")
            parent_id = request.POST.get("parent")
            reply = form.save(commit=False)

            reply.user = Profile.objects.get(user__id=request.user.id)
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            return redirect(post_url + "#" + str(reply.id))

    return redirect("/")


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = "core/post_form.html"
    success_url = reverse_lazy("core:post_list")

    def form_valid(self, form):
        form.instance.author = Profile.objects.get(user__id=self.request.user.id)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    success_url = ""

    def get_object(self, queryset=None):
        obj = super(PostUpdateView, self).get_object(queryset)
        if obj.author.id != self.request.user.profile.id:
            raise Http404("You don't own this object")
        return obj


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy("core:post_list")

    def get_object(self, queryset=None):
        obj = super(PostDeleteView, self).get_object(queryset)
        if obj.author.id != self.request.user.profile.id:
            raise Http404("You don't own this object")
        return obj


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = ""

    def get_object(self, queryset=None):
        obj = super(ProfileUpdateView, self).get_object(queryset)
        if obj.id != self.request.user.profile.id:
            raise Http404("You don't own this object")
        return obj

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        user = self.request.user
        print(context)
        context["form"] = ProfileForm(
            instance=self.request.user.profile,
            initial={
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }
        )
        return context

    def form_valid(self, form):
        profile = form.save()
        user = profile.user
        user.username = form.cleaned_data["username"]
        user.last_name = form.cleaned_data["last_name"]
        user.first_name = form.cleaned_data["first_name"]
        user.email = form.cleaned_data["email"]
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("core:profile_detail", kwargs={"pk": self.object.id})


class ProfileDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Profile
    success_url = ""

    def get_object(self, queryset=None):
        obj = super(ProfileDeleteView, self).get_object(queryset)
        if obj.id != self.request.user.profile.id:
            raise Http404("You don't own this object")
        return obj
