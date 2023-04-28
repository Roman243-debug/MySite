from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post, User

User = get_user_model()


field_verboses = {
    'text': 'Текст',
    'pub_date': 'Дата Публикации',
    'author': 'Автор',
    'group': 'Группа',
}

HELP_FIELD = {
    'text': 'Введите текст поста',
    'group': 'Выберите группу',
}

SMALL_GIF = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B')


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Титл',
            slug='Слаг',
            description='Описание',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Текст',
        )

    def test_models_have_correct_object_names(self):
        """Проверка модели объекта имени"""
        str_group = self.group
        title_group = self.group.title
        self.assertEqual(title_group, str(str_group))
        str_post = self.post
        text_post = self.post.text[:15]
        self.assertEqual(text_post, str(str_post))

    def test_verbose_name(self):
        """Тест"""
        self.post = PostModelTest.post
        for field, value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).verbose_name, value)

    def test_help_text_in_post_model(self):
        """Test help_text"""
        self.post = PostModelTest.post
        for field, value in HELP_FIELD.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).help_text, value)
