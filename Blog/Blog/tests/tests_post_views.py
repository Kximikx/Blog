from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from myblog.models import Post

class PostViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(
            author=self.user,
            title="Test Post",
            text="Test content",
            published_date=timezone.now()
        )

    def test_index_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myblog/index.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertTemplateUsed(response, 'myblog/post_detail.html')

    def test_post_new_view_not_logged_in(self):
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 302)  

    def test_post_new_view_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myblog/post_edit.html')

    def test_post_create(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post_new'), {
            'title': 'New Post',
            'text': 'New content'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Post.objects.count(), 2)

    def test_post_edit_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post_edit', args=[self.post.pk]), {
            'title': 'Updated Title',
            'text': 'Updated content'
        })
        self.assertEqual(response.status_code, 302)  
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_post_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Post.objects.count(), 0)
