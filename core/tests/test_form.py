from django.test import TestCase
from django.contrib.auth.models import User
from core.forms import CommentForm, SignUpForm, PostSearchForm, PostForm
from core.models import Post


class CommentFormTest(TestCase):
    def test_comment_form_valid_data(self):
        user = User(username="testuser")
        user.save()
        form_data = {"body": "Test Comment"}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_blank_data(self):
        form_data = {"body": ""}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["body"], ["This field is required."])


class SignUpFormTest(TestCase):
    def test_signup_form_valid_data(self):
        form_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword"
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_blank_data(self):
        form_data = {}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["username"], ["This field is required."])


class PostSearchFormTest(TestCase):
    def test_post_search_form_valid_data(self):
        form_data = {"title": "Search Term"}
        form = PostSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_search_form_blank_data(self):
        form_data = {}
        form = PostSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class PostFormTest(TestCase):
    def test_post_form_valid_data(self):
        user = User(username="testuser")
        user.save()
        form_data = {
            "title": "Test Post",
            "image": None,
            "content": "Test content",
            "tags": "tag1,tag2",
            "status": "draft"
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_form_duplicate_title(self):
        user = User(username="testuser")
        user.save()
        Post.objects.create(title="Test Post", author=user.profile)
        form_data = {
            "title": "Test Post",
            "image": None,
            "content": "Test content",
            "tags": "tag1,tag2",
            "status": "draft"
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], ["A post with that title already exists."])
