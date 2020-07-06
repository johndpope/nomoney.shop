""" Abstract TestCase for all app tests """
from abc import ABC
from django.test import TestCase as BaseTestCase
from django.test import Client as BaseClient
from django.urls.base import reverse
from testdb import TestDB


class DummyTestCase(BaseTestCase):
    pass


class Client(BaseClient):

    def __init__(self, *args, **kwargs):
        self.tester = DummyTestCase()
        super(Client, self).__init__(*args, **kwargs)

    def get200(self, url_name, url_args=None, url_kwargs=None):
        url = self.url(url_name, url_args, url_kwargs)
        response = self.get(url)
        self.tester.assertIs(response.status_code, 200)
        return response

    def get302(self, url_name, url_args=None, url_kwargs=None):
        url = self.url(url_name, url_args, url_kwargs)
        response = self.get(url)
        self.tester.assertEqual(response.status_code, 302)
        return response

    def post302(self, url_name, url_args=None, url_kwargs=None, data={}):
        url = self.url(url_name, url_args, url_kwargs)
        response = self.post(url, data=data)
        self.tester.assertEqual(response.status_code, 302)
        return response

    def getpost(self, url_name, url_args=None, url_kwargs=None, data={}):
        self.get200(url_name, url_args=url_args, url_kwargs=url_kwargs)
        self.post302(url_name, url_args=url_args, url_kwargs=url_kwargs,
                     data=data)

    def url(self, url_name, url_args=None, url_kwargs=None):
        url_args = (str(url_args), ) if isinstance(url_args, (str, int, )) \
            else url_args
        return reverse(url_name, args=url_args, kwargs=url_kwargs)


class TestCase(ABC, BaseTestCase):
    """ inherit this class for all tests """

    def run(self, *args, **kwargs):  # pylint: disable=arguments-differ
        response = None
        if self.__module__ != 'tests_abc':
            response = super().run(*args, **kwargs)
        return response

    def setUp(self):
        self.testdb = TestDB
        self.testdb.USER_COUNT = 10
        self.testdb.DEAL_COUNT = 10
        self.testdb.LISTING_COUNT = 50
        self.testdb.PRINT_STEPS = False
        self.testdb.setup()
        self.user = Client()
        self.user.login(
            username=self.testdb.USER_NAME,
            password=self.testdb.USER_PASSWORD,
            )
        self.anon = Client()

        self.demo = TestDB.demo
        self.demo1 = TestDB.demo1
        self.deal = TestDB.deal
        self.location = TestDB.location
        self.guild = TestDB.guild

    def random_object(self, model):
        return TestDB.random_object(model)

    def test_apps(self):
        """ Tests for the apps.py of this module """
        from importlib import import_module
        module_title = self.__module__.split('.')[0]
        module = import_module(module_title + '.apps')
        class_ = getattr(module, module_title.title() + 'Config')
        self.assertEqual(class_.__name__, module_title.title() + 'Config')
