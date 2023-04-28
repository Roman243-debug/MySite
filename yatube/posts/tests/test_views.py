from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Для себя - Создание юсер
        cls.author = User.objects.create_user(username='auth')
        # Создание Группы
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание группы',
        )
        # Создание Поста
        cls.post = Post.objects.create(
            text='Тестовый текст поста',
            author=cls.author,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "reverse(name): имя_html_шаблона"
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',

            reverse('posts:group_list', kwargs=(
                {'slug': f'{self.post.group.slug}'})): 'posts/group_list.html',

            reverse('posts:profile', kwargs=(
                {'username': f'{self.author}'})): 'posts/profile.html',

            reverse('posts:post_detail', kwargs=(
                {'post_id': f'{self.post.id}'})): 'posts/post_detail.html',

            reverse('posts:post_edit', kwargs=(
                {'post_id': f'{self.post.id}'})): 'posts/create_post.html',

            reverse('posts:post_create'): 'posts/create_post.html',
        }

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='UserHasNoName')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание группы',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        post_list = []
        for i in range(12):
            post_list.append(Post(
                text=f'Тестовый пост {i}',
                group=self.group,
                author=self.user)
            )
        Post.objects.bulk_create(post_list)

    def test_first_page_contains_ten_records(self):
        """1я страница содержит 10 записей"""
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        """2я страница содержит 3 записи"""
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)
