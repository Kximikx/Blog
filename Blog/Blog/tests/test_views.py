# blog/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from myblog.models import Post

User = get_user_model()

class CreatePostIntegrationTest(TestCase):
    def setUp(self):
        # Створюємо тестового користувача і логінуємо його
        self.user = User.objects.create_user(
            username='testuser',
            password='secret'
        )
        self.client.login(username='testuser', password='secret')

    def test_create_post_view(self):
        # Дані форми для створення нового поста
        form_data = {
            'title': 'Новий пост',
            'text': 'Це вміст поста.'
        }

        # Відправляємо POST-запит для створення поста
        response = self.client.post(reverse('post_new'), data=form_data)

        # Перевіряємо, що відбувся редірект (статус 302)
        self.assertEqual(response.status_code, 302)

        # Перевіряємо, що пост зберігся в базі даних
        self.assertTrue(Post.objects.filter(title='Новий пост').exists())

        # Отримуємо створений пост і перевіряємо його дані
        post = Post.objects.get(title='Новий пост')
        self.assertEqual(post.text, 'Це вміст поста.')
        self.assertEqual(post.author, self.user)
