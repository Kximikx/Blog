from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from  myblog.models import Post

class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_post_creation(self):
        """Тест створення посту"""
        post = Post.objects.create(
            author=self.user,
            title="Test Post",
            text="This is a test post.",
        )
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.text, "This is a test post.")
        self.assertEqual(post.author, self.user)
        self.assertIsNone(post.published_date) 

    def test_publish_method(self):
        """Тест методу publish()"""
        post = Post.objects.create(
            author=self.user,
            title="Test Post",
            text="This is a test post.",
        )
        post.publish() 
        self.assertIsNotNone(post.published_date) 
        self.assertLessEqual(post.published_date, timezone.now())

    def test_post_str_method(self):
        """Тест методу __str__()"""
        post = Post.objects.create(
            author=self.user,
            title="Test Post",
            text="This is a test post.",
        )
        self.assertEqual(str(post), "Test Post")

    def test_edit_post(self):
        """Тест редагування посту"""
        post = Post.objects.create(
            author=self.user,
            title="Initial Title",
            text="Initial Content",
        )
        post.title = "Updated Title"
        post.text = "Updated Content"
        post.save()

        self.assertEqual(post.title, "Updated Title")
        self.assertEqual(post.text, "Updated Content")

    def test_delete_post(self):
        """Тест видалення посту"""
        post = Post.objects.create(
            author=self.user,
            title="Test Post to Delete",
            text="This post will be deleted.",
        )
        post_id = post.id
        post.delete()
        self.assertFalse(Post.objects.filter(id=post_id).exists())
