from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from posts.models import Post, User

INDEX = reverse('posts:index')


@classmethod
class CacheTests(TestCase):
    def setUpClass(cls):
        super().setUpClass()
        cls.test = User.objects.create(username='cache')
        cls.post = Post.objects.create(
            text='Введите текст поста',
            author=cls.test,
        )

    def test_pages_uses_correct_template(self):
        """Кэширование данных на главной странице работает корректно"""
        response = self.client.get(INDEX)
        cached_response_content = response.content
        Post.objects.create(text='Текст', author=self.test)
        response = self.client.get(INDEX)
        self.assertEqual(cached_response_content, response.content)
        cache.clear()
        response = self.client.get(INDEX)
        self.assertNotEqual(cached_response_content, response.content)
