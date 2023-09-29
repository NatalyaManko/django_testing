from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestListPage(TestCase):

    NOTE_TEXT = 'Текст комментария'
    NOTE_TITLE = 'Ням Хрю'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Львёнок Толстый')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.another_user = User.objects.create(username='Мимо Крокодил')
        cls.another_user_client = Client()
        cls.another_user_client.force_login(cls.another_user)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
            slug='slug'
        )
        cls.list_url = reverse('notes:list')
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
        }

    def test_notes_in_list_for_author(self):
        response = self.author_client.get(self.list_url)
        notes_list = response.context['object_list']
        note_object = notes_list[0]
        self.assertIn(note_object, notes_list)

    def test_notes_list_for_different_users(self):
        users_notes = (
            (self.author_client, True),
            (self.another_user_client, False),
        )
        for user, notes_list in users_notes:
            with self.subTest(user=user, notes_list=notes_list):
                response = user.get(self.list_url)
                notes_object = self.note in response.context['object_list']
                self.assertEqual(notes_object, notes_list)

    def test_authorized_client_has_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for path, args in urls:
            with self.subTest(path=path):
                response = self.author_client.get(reverse(path, args=args))
                form = response.context.get('form')
                self.assertIsInstance(form, NoteForm)
                self.assertIn('form', response.context)
