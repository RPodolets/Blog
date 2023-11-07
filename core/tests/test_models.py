from django.contrib.auth.models import User
from django.test import TestCase

from core.models import Profile, Post, Comment


class ProfileModelTest(TestCase):
    def test_profile_str_representation(self):
        user = User(username="testuser")
        user.save()
        profile = Profile(user=user)
        self.assertEqual(str(profile), "testuser")

    def test_profile_create_or_update_user_profile(self):
        user = User(username="testuser")
        user.save()
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_post_str_representation(self):
        post = Post(title="Test Post", author=self.user.profile)
        self.assertEqual(str(post), "Test Post")

    def test_post_get_absolute_url(self):
        post = Post.objects.create(title="Test Post", author=self.user.profile)
        expected_url = f"/{post.slug}/"
        self.assertEqual(post.get_absolute_url(), expected_url)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.post = Post.objects.create(title="Test Post", author=self.user.profile)

    def test_comment_str_representation(self):
        comment = Comment(post=self.post, user=self.user.profile, body="Test Comment")
        self.assertEqual(str(comment), "Test Comment")
