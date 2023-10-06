from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset().filter(status="published")
        return queryset.prefetch_related("tags").select_related("author", "author__user")


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")

    def __str__(self):
        return str(self.user)

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date="publish")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to="featured_image/%Y/%m/%d/")
    content = RichTextUploadingField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    views = models.IntegerField(default=0)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:post_detail", args=[self.slug])

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True).prefetch_related("user")

    def update_views(self, *args, **kwargs):
        self.views = self.views + 1
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.body

    def get_comments(self):
        return Comment.objects.filter(parent=self).prefetch_related("profile").filter(active=True)
