import pytest
from django.conf import settings


@pytest.mark.django_db
def test_news_count(client, many_news, home_url):
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, many_news, home_url):
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, news, many_comment, detail_url):
    response = client.get(detail_url)
    object_list = response.context['news'].comment_set.all()
    all_created = [comment.created for comment in object_list]
    sorted_created = sorted(all_created, reverse=False)
    assert all_created == sorted_created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, news, detail_url):
    response = author_client.get(detail_url)
    assert 'form' in response.context
