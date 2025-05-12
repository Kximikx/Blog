from django.test import TestCase
from django.contrib.auth import get_user_model
from myblog.models import Post

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        # Створюємо тестового користувача
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        # Створюємо пост з автором
        self.post = Post.objects.create(
            author=self.user,
            title='Тестовий заголовок',
            text='Деякий контент'
        )

    def test_post_str_method(self):
        # Перевірка, чи повертає метод __str__ правильне значення
        self.assertEqual(str(self.post), 'Тестовий заголовок')
