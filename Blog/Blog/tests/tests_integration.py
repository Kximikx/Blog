from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from  myblog.models import Post
from django.utils import timezone

class PostIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(
            author=self.user,
            title="Initial Title",
            text="Initial text",
            published_date=timezone.now()
        )
        self.client.login(username='testuser', password='password')

    def test_edit_post(self):
        """Перевірка редагування посту"""
        url = reverse('post_edit', kwargs={'pk': self.post.pk})
        response = self.client.post(url, {
            'title': 'Updated Title',
            'text': 'Updated text',
        })
        self.post.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.text, 'Updated text')

    def test_delete_post(self):
        """Перевірка видалення посту"""
        url = reverse('post_delete', kwargs={'pk': self.post.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

