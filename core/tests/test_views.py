from django.contrib.auth import get_user_model
from django.http import HttpResponseNotFound
from django.test import TestCase
from django.urls import reverse
from taggit.models import Tag

from core.forms import PostSearchForm
from core.models import Post, Comment

POST_LIST_URL = reverse("core:post_list")

PROFILE_DETAIL_URL = reverse("core:profile_detail", kwargs={"pk": 0})
PROFILE_UPDATE_URL = reverse("core:profile_update", kwargs={"pk": 0})
PROFILE_DELETE_URL = reverse("core:profile_delete", kwargs={"pk": 0})


class TestUnauthorisedAccess(TestCase):
    def test_post_list_anonymous_user_access_denied(self) -> None:
        response = self.client.get(POST_LIST_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_profile_detail_anonymous_user_access_denied(self) -> None:
        response = self.client.get(PROFILE_DETAIL_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_profile_update_anonymous_user_access_denied(self) -> None:
        response = self.client.get(PROFILE_DETAIL_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_profile_delete_anonymous_user_access_denied(self) -> None:
        response = self.client.get(PROFILE_DETAIL_URL)
        self.assertNotEquals(response.status_code, 200)


class PostListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

        self.post1 = Post.objects.create(
            title="Test Post 1",
            author=self.user.profile,
            status="published",
        )
        self.post2 = Post.objects.create(
            title="Test Post 2",
            author=self.user.profile,
            status="published",
        )

        self.tag1 = Tag.objects.create(name="Tag1")
        self.tag2 = Tag.objects.create(name="Tag2")

        self.post1.tags.add(self.tag1)
        self.post2.tags.add(self.tag2)

    def test_post_list_view(self):
        self.client.login(username="testuser", password="testpassword")

        response = self.client.get(reverse("core:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/post_list.html")
        self.assertContains(response, "Test Post 1")
        self.assertContains(response, "Test Post 2")
        self.assertIsInstance(response.context["search_form"], PostSearchForm)
        self.assertQuerysetEqual(
            response.context["tag_list"],
            Tag.objects.all(),
            ordered=False
        )

    def test_post_list_view_with_title_filter(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("core:post_list") + "?title=Test Post 1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post 1")
        self.assertNotContains(response, "Test Post 2")

    def test_post_list_view_with_tag_filter(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("core:post_tag", kwargs={"tag_slug": self.tag1.name}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post 1")
        self.assertNotContains(response, "Test Post 2")


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

        self.post = Post.objects.create(
            title="Test Post",
            author=self.user.profile,
            status="published",
        )

        self.tag = Tag.objects.create(name="Test Tag")
        self.post.tags.add(self.tag)

        self.client.login(username="testuser", password="testpassword")

    def test_post_detail_view(self):
        response = self.client.get(reverse("core:post_detail", kwargs={"post": self.post.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/post_detail.html")

        self.assertContains(response, "Test Post")

    def test_post_detail_view_with_draft_post(self):
        get_user_model().objects.create_user(
            username="user2", password="pass2"
        )
        self.client.login(username="user2", password="pass2")

        self.post.status = "draft"
        self.post.save()

        response = self.client.get(reverse("core:post_detail", kwargs={"post": self.post.slug}))

        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_with_nonexistent_post(self):
        response = self.client.get(reverse("core:post_detail", kwargs={"post": "nonexistent-slug"}))

        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, HttpResponseNotFound)


class PostUpdateDeleteViewTest(TestCase):
    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

        self.post = Post.objects.create(
            title="Test Post",
            author=self.user.profile,
            status="published",
        )

    def test_post_update_view_with_author(self):
        self.client.login(username="testuser", password="testpassword")

        url = reverse("core:post_update", kwargs={"slug": self.post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_post_update_view_with_non_author(self):
        get_user_model().objects.create_user(
            username="otheruser", password="otherpassword"
        )

        self.client.login(username="otheruser", password="otherpassword")

        url = reverse("core:post_update", kwargs={"slug": self.post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_post_delete_view_with_author(self):
        self.client.login(username="testuser", password="testpassword")

        url = reverse("core:post_delete", kwargs={"slug": self.post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
