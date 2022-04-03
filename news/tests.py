from urllib import response
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import News, Category


class GetPageTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.blog = Category.objects.create(name='test')
        self.user = User.objects.create(username='test', password='test')
        self.news = News.objects.create(title='test',
                                        text='test',
                                        blog=self.blog,
                                        owner=self.user)

    def doCleanup(self):
        self.blog.delete()
        self.user.delete()
        self.news.delete()

    def get_page(self, url: str, status_code: int, error_message: str):
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code, error_message)

    def test_get_home(self):
        self.get_page("/", 200, "Can't get home page.")

    def test_get_blogs_list(self):
        self.get_page("/blogs/", 200, "Can't get blogs list page.")

    def test_get_news_item(self):
        self.get_page("/news/{0}/".format(self.news.id), 200,
                      "Can't get news item page.")

    def test_get_blog_item(self):
        self.get_page("/blog/{0}/".format(self.blog.id), 200,
                      "Can't get blog item page.")


class NewsAddEditDeleteViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.blog = Category.objects.create(name='test')
        self.user = User.objects.create_superuser(username='test',
                                                  password='test')
        self.news_kwargs = {
            'title': 'test1',
            'text': 'test1',
            'blog': self.blog,
            'owner': self.user
        }
        self.news_form_data = {
            'title': 'test2',
            'text': 'test2',
            'blog': str(self.blog.id),
            'owner': str(self.user.id)
        }
        self.client.login(username='test', password='test')

    def doCleanup(self):

        def delete_news(title):
            news = News.objects.filter(title=title).first
            if news:
                news.delete()

        self.blog.delete()
        self.user.delete()
        delete_news(self.news_kwargs['title'])
        delete_news(self.news_form_data['title'])

    def get_page(self, url: str, status_code: int, error_message: str):
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code, error_message)

    def test_news_delete(self):
        news = News.objects.create(**self.news_kwargs)
        response = self.client.post('/news/{0}/delete/'.format(news.id))
        self.assertEqual(response.status_code, 302, "Can't delete news.")
        news = News.objects.filter(id=news.id).first()
        self.assertIsNone(news, 'Error in sending data on news delete page.')

    def test_news_add(self):
        url = '/news/add/'
        self.get_page(url, 200, "Can't get news add page.")
        response = self.client.post(url, self.news_form_data)
        self.assertEqual(response.status_code, 302, "Can't add news.")
        news = News.objects.filter(title=self.news_form_data['title']).first()
        self.assertIsNotNone(news, 'Error in sending data on news add page.')
        news.delete()

    def test_news_edit(self):
        news = News.objects.create(**self.news_kwargs)
        url = '/news/{}/edit/'.format(news.id)
        self.get_page(url, 200, "Can't get news edit page.")
        response = self.client.post(url, self.news_form_data)
        self.assertEqual(response.status_code, 302, "Can't add news.")
        news = News.objects.filter(title=self.news_form_data['title']).first()
        self.assertIsNotNone(news, 'Error in sending data on news edit page.')
        news.delete()
