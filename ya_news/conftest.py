from datetime import datetime as dt
from datetime import timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

URL_DETAIL = ('news:detail')
URL_EDIT = ('news:edit')
URL_DELETE = ('news:delete')
URL_HOME = ('news:home')


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    news.date = dt(year=2020, month=1, day=1)
    return news


@pytest.fixture
def many_news():
    today = dt.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        text='Текст',
        author=author,
    )
    comment.created = dt(year=2020, month=1, day=1)
    return comment


@pytest.fixture
def many_comment(news, author):
    today = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            text=f'Просто текст. {index}',
            author=author
        )
        comment.created = today + timedelta(days=index)
        comment.save()


@pytest.fixture
def pk_for_args_comment(comment):
    return comment.pk,


@pytest.fixture
def pk_for_args_news(news):
    return news.pk,


@pytest.fixture
def form_data():
    return {'text': 'Новый текст'}


@pytest.fixture
def home_url():
    return reverse(URL_HOME)


@pytest.fixture
def detail_url(pk_for_args_news):
    return reverse(URL_DETAIL, args=(pk_for_args_news))


@pytest.fixture
def edit_url(pk_for_args_comment):
    return reverse(URL_EDIT, args=(pk_for_args_comment))


@pytest.fixture
def delete_url(pk_for_args_comment):
    return reverse(URL_DELETE, args=(pk_for_args_comment))
