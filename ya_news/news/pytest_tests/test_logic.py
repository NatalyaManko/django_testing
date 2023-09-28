from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(author_client, author, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, (url + '#comments'))
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


def test_user_cant_use_bad_words(admin_client, news, author, form_data):
    url = reverse('news:detail', args=(news.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = admin_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )


def test_author_can_edit_comment(
    author_client,
    author,
    form_data,
    news,
    comment
):
    url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(url, form_data)
    assertRedirects(
        response,
        reverse(
            'news:detail',
            args=(news.id,)
        ) + '#comments'
    )
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert comment.author == author


def test_user_cant_edit_comment(admin_client, form_data, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = admin_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text
    assert comment.author == comment_from_db.author


def test_author_can_delete_comment(author_client, comment, news):
    url = reverse('news:delete', args=(comment.id,))
    response = author_client.post(url)
    assertRedirects(
        response,
        reverse(
            'news:detail',
            args=(news.id,)
        ) + '#comments'
    )
    assert Comment.objects.count() == 0


def test_other_user_cant_delete_note(admin_client, form_data, comment, news):
    url = reverse('news:delete', args=(comment.id,))
    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
