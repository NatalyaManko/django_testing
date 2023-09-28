
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestListPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Львёнок Толстый')
        cls.another_user = User.objects.create(username='Мимо Крокодил')
        all_notes = [
            Note(
                title=f'Заголовок {index}',
                text='Просто текст.',
                author=cls.author,
                slug=f'slug{index}'
            )
            for index in range(10)
        ]
        Note.objects.bulk_create(all_notes)
        cls.list_url = reverse('notes:list')

    def test_note_in_list_for_author(self):
        self.client.force_login(self.author)
        response = self.client.get(self.list_url)
        object_list = response.context['object_list']
        note_object = object_list[0]
        self.assertIn(note_object, object_list)

    def test_notes_list_for_different_users(self):
        self.client.force_login(self.another_user)
        response = self.client.get(self.list_url)
        object_list = response.context['object_list']
        self.assertNotIn(
            Note(
                title='Заголовок 1',
                text='Просто текст.',
                slug='slug1'
            ),
            object_list
        )

    def test_authorized_client_has_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', ('slug1',)),
        )
        for path, args in urls:
            with self.subTest(path=path):
                self.client.force_login(self.author)
                response = self.client.get(reverse(path, args=args))
                self.assertIn('form', response.context)
