from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:detail', pytest.lazy_fixture('pk_for_args_news'))
    )
)
def test_pages_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        (pytest.lazy_fixture('edit_url')),
        (pytest.lazy_fixture('delete_url')),
    )
)
def test_redirects_anonymous(client, name):
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={name}'
    response = client.get(name)
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    'parametrize_client, expected_status',
    (
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
    )
)
@pytest.mark.parametrize(
    'name_url',
    (
        (pytest.lazy_fixture('edit_url')),
        (pytest.lazy_fixture('delete_url')),
    )
)
def test_comment_edit_delete_pages_for_users(
    parametrize_client,
    expected_status,
    name_url
):
    response = parametrize_client.get(name_url)
    assert response.status_code == expected_status
