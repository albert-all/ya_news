# news/tests/test_content.py
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
# Импортируем функцию reverse(), она понадобится для получения адреса страницы.
from django.urls import reverse

from news.models import Comment, News
from datetime import datetime, timedelta


User = get_user_model()


class TestHomePage(TestCase):
    # Вынесем ссылку на домашнюю страницу в атрибуты класса.
    HOME_URL = reverse('news:home')

    @classmethod
    def setUpTestData(cls):
        all_news = [
            News(title=f'Новость {index}', text='Просто текст.')
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        ]
        News.objects.bulk_create(all_news)

    def test_news_count(self):
        # Загружаем главную страницу.
        response = self.client.get(self.HOME_URL)
        # Код ответа не проверяем, его уже проверили в тестах маршрутов.
        # Получаем список объектов из словаря контекста.
        object_list = response.context['object_list']
        # Определяем количество записей в списке.
        news_count = object_list.count()
        # Проверяем, что на странице именно 10 новостей.
        self.assertEqual(news_count, settings.NEWS_COUNT_ON_HOME_PAGE)


class TestDetailPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(
            title='Тестовая новость', text='Просто текст.'
        )
        # Сохраняем в переменную адрес страницы с новостью:
        cls.detail_url = reverse('news:detail', args=(cls.news.id,))
        cls.author = User.objects.create(username='Комментатор')
        # Запоминаем текущее время:
        now = datetime.now()
        # Создаём комментарии в цикле.
        for index in range(10):
            # Создаём объект и записываем его в переменную.
            comment = Comment.objects.create(
                news=cls.news, author=cls.author, text=f'Tекст {index}',
            )
            # Сразу после создания меняем время создания комментария.
            comment.created = now + timedelta(days=index)
            # И сохраняем эти изменения.
            comment.save()

            
