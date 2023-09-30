import random
from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, detail_url, form_data):
    comment_count = Comment.objects.count()
    response = client.post(detail_url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={detail_url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == comment_count


def test_user_can_create_comment(
    author,
    author_client,
    news,
    detail_url,
    form_data
):
    response = author_client.post(detail_url, data=form_data)
    assertRedirects(response, (detail_url + '#comments'))
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author
    assert new_comment.news == news


def test_user_cant_use_bad_words(admin_client, detail_url):
    bad_words_data = {
        'text': f'Какой-то текст, {random.choice(BAD_WORDS)}, еще текст'
    }
    response = admin_client.post(detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )


def test_author_can_edit_comment(
    author,
    author_client,
    news,
    comment,
    edit_url,
    detail_url,
    form_data
):
    response = author_client.post(edit_url, form_data)
    assertRedirects(response, (detail_url + '#comments'))
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert comment.author == author
    assert comment.news == news


def test_user_cant_edit_comment(
    admin_client,
    news,
    comment,
    edit_url,
    pk_for_args_comment,
    form_data
):
    response = admin_client.post(edit_url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=pk_for_args_comment[0])
    assert comment.text == comment_from_db.text
    assert comment.author == comment_from_db.author
    assert comment.news == news


def test_author_can_delete_comment(author_client, delete_url, detail_url):
    comment_count = Comment.objects.count()
    response = author_client.post(delete_url)
    assertRedirects(
        response,
        detail_url + '#comments'
    )
    assert Comment.objects.count() < comment_count


def test_other_user_cant_delete_note(admin_client, delete_url, form_data):
    comment_count = Comment.objects.count()
    response = admin_client.post(delete_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comment_count
