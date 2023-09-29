import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('news:home',),
)
def test_news_count(name, client, many_news):
    url = reverse(name)
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('news:home',),
)
def test_news_order(name, client, many_news):
    url = reverse(name)
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('news:detail',),
)
def test_comments_order(name, client, news, many_comment):
    url = reverse(name, args=(news.id,))
    response = client.get(url)
    object_list = response.context['news'].comment_set.all()
    all_created = [comment.created for comment in object_list]
    sorted_created = sorted(all_created, reverse=False)
    assert all_created == sorted_created


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        ('news:detail'),
    )
)
def test_anonymous_client_has_no_form(name, client, news):
    url = reverse(name, args=(news.id,))
    response = client.get(url)
    assert 'form' not in response.context


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        ('news:detail'),
    )
)
def test_authorized_client_has_form(name, author_client, news):
    url = reverse(name, args=(news.id,))
    response = author_client.get(url)
    assert 'form' in response.context
