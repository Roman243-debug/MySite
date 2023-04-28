from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User

User = get_user_model()

USER = 'author1'
CREATE_NAME = 'posts:post_create'
POST_EDIT_NAME = 'posts:post_edit'
PROFILE_NAME = 'posts:profile'

SMALL_GIF = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B')


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title=('Заголовок для тестовой группы'),
            slug='test_slug5',
            description='Тестовое описание'
        )

    def setUp(self):
        self.guest_client = Client()
        # Создаём авторизованный клиент
        self.user = User.objects.create_user(username='author1')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post(self):
        """Тест создания Поста"""
        count_posts = Post.objects.count()
        form_data = {
            'text': 'Данные из формы',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse(CREATE_NAME),
            data=form_data,
            follow=True,
        )
        new_post = Post.objects.get(id=self.group.id)
        self.assertEqual(Post.objects.count(), count_posts + 1)
        self.assertRedirects(response, reverse('posts:profile',
                             kwargs={'username': self.user.username}))
        self.assertEqual(new_post.text, form_data['text'])
        self.assertEqual(new_post.author.username, self.user.username)

    def test_guest_new_post(self):
        """Тест нового поста"""
        # неавторизоанный не может создавать посты
        form_data = {
            'text': 'Пост от неавторизованного пользователя',
            'group': self.group.id
        }
        self.guest_client.post(
            reverse(CREATE_NAME),
            data=form_data,
            follow=True,
        )
        self.assertFalse(Post.objects.filter(
            text='Пост от неавторизованного пользователя'))

    def test_authorized_edit_post(self):
        """Тест авторизованного поста"""
        # авторизованный может редактировать
        post = Post.objects.create(
            text='Измененный текст',
            author=self.user,
            group=self.group,
        )
        new_group = Group.objects.create(
            title='Титл',
            slug='Слаг',
            description='Описание',
        )
        form_data = {
            'text': 'Измененный текст',
            'group': new_group.id,
        }
        response_edit = self.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={
                        'post_id': post.id
                    },),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response_edit.status_code,
                         HTTPStatus.OK,)
        self.assertEqual(post.text, form_data['text'])

        old_group_response = self.authorized_client.get(
            reverse('posts:group_list', args=(self.group.slug,))
        )
        self.assertEqual(old_group_response.context
                         ['page_obj'].paginator.count, 0)
