# conftest.py
from datetime import datetime as dt
from datetime import timedelta

import pytest
from django.conf import settings
from django.utils import timezone

from news.models import Comment, News


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
    all_comment = [
        Comment(
            news=news,
            text=f'Просто текст. {index}',
            author=author,
            created=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    Comment.objects.bulk_create(all_comment)


@pytest.fixture
def pk_for_args_comment(comment):
    return comment.pk,


# Добавляем фикстуру form_data
@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст',
    }
