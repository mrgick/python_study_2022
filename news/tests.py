from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from .models import News, Category
from .forms import NewsForm, CategoryForm
from .decorators import check_obj_exist, check_owner


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
        self.news.delete()
        self.blog.delete()
        self.user.delete()

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
            'blog': str(self.blog.id)
        }
        self.client.login(username='test', password='test')

    def doCleanup(self):

        def delete_news(title):
            news = News.objects.filter(title=title).first
            if news:
                news.delete()

        delete_news(self.news_kwargs['title'])
        delete_news(self.news_form_data['title'])
        self.blog.delete()
        self.user.delete()

    def get_page(self, url: str, status_code: int, error_message: str):
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code, error_message)

    def test_news_delete(self):
        news = News.objects.create(**self.news_kwargs)
        response = self.client.post('/news/{0}/delete/'.format(news.id))
        self.assertEqual(response.status_code, 302, "Can't delete news.")
        news = News.objects.filter(id=news.id).first()
        self.assertIsNone(news, 'Error in sending data on news delete page.')

    def test_NewsForm(self):
        form = NewsForm(self.news_form_data)
        self.assertTrue(form.is_valid(), 'Error with NewsForm.')

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
        url = '/news/{0}/edit/'.format(news.id)
        self.get_page(url, 200, "Can't get news edit page.")
        response = self.client.post(url, self.news_form_data)
        self.assertEqual(response.status_code, 302, "Can't add news.")
        news = News.objects.filter(title=self.news_form_data['title']).first()
        self.assertIsNotNone(news, 'Error in sending data on news edit page.')
        news.delete()


class DecoratorsTestCase(TestCase):

    def setUp(self):
        self.blog = Category.objects.create(name='test')
        self.user1 = User.objects.create_user(username='test1', password='t')
        self.user2 = User.objects.create_user(username='test2', password='t')
        self.news_kwargs = {
            'title': 'test1',
            'text': 'test1',
            'blog': self.blog,
            'owner': self.user1
        }
        self.news = News.objects.create(**self.news_kwargs)

    def doCleanup(self):
        self.news.delete()
        self.blog.delete()
        self.user1.delete()
        self.user2.delete()

    def test_obj_exist(self):

        @check_obj_exist(News, 'news_id')
        def simple_view(request, news_id):
            return HttpResponse('test view')

        request = HttpRequest()
        response = simple_view(request, news_id=self.news.id)
        self.assertEqual(response.status_code, 200,
                         'Error checks obj exist decoration.')
        response = simple_view(request, news_id=self.news.id + 1)
        self.assertEqual(response.status_code, 404,
                         'Error checks obj not exist decoration.')

    def test_check_owner(self):

        @check_owner
        def simple_view(request, news_id):
            return HttpResponse('test view')

        request = HttpRequest()
        request.user = self.user1
        response = simple_view(request, news_id=self.news.id)
        self.assertEqual(response.status_code, 200,
                         'Error checks owner decoration.')
        request.user = self.user2
        response = simple_view(request, news_id=self.news.id)
        self.assertEqual(response.status_code, 403,
                         'Error checks not owner decoration.')


class BlogFormTestCase(TestCase):

    def setUp(self):
        self.form_data = {'name': 'testblogform'}
        self.user = User.objects.create_superuser(username='t', password='t')
        self.client = Client()
        self.client.login(username='t', password='t')

    def doCleanup(self):
        self.user.delete()
        blog = Category.objects.filter(name=self.form_data['name']).first()
        if blog:
            blog.delete()

    def test_form(self):
        form = CategoryForm(self.form_data)
        self.assertTrue(form.is_valid(), 'Error with CategoryForm.')

    def test_blog_add(self):
        url = '/blog/add/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         "Can't get to blog add page.")
        response = self.client.post(url, self.form_data)
        self.assertEqual(response.status_code, 200,
                         "Error in sending data on blog add page.")
        blog = Category.objects.filter(name=self.form_data['name']).first()
        self.assertIsNotNone(blog, 'Error in sending data on news add page.')
        blog.delete()