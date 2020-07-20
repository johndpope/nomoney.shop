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

    def test_url(self, url, method, status_code, data=None):
        data = data or {}
        if method.lower() == 'get':
            response = self.get(url)
        elif method.lower() == 'post':
            response = self.post(url, data=data)
        self.tester.assertEqual(response.status_code, status_code)
        return response

    def get200(self, url_name, url_args=None, url_kwargs=None):
        url = self.url(url_name, url_args, url_kwargs)
        return self.test_url(url, 'get', 200)

    def get302(self, url_name, url_args=None, url_kwargs=None):
        url = self.url(url_name, url_args, url_kwargs)
        return self.test_url(url, 'get', 302)

    def post302(self, url_name, url_args=None, url_kwargs=None, data=None):
        url = self.url(url_name, url_args, url_kwargs)
        return self.test_url(url, 'post', 302, data=data)

    def getpost(self, url_name, url_args=None, url_kwargs=None, data=None):
        self.get200(url_name, url_args=url_args, url_kwargs=url_kwargs)
        self.post302(url_name, url_args=url_args, url_kwargs=url_kwargs,
                     data=data)

    @staticmethod
    def url(url_name, url_args=None, url_kwargs=None):
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
        self.testdb.USER_COUNT = 3
        self.testdb.DEAL_COUNT = 5
        self.testdb.LISTING_COUNT = 20
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
        self.market = TestDB.market

    @staticmethod
    def random_object(model):
        """ get a random object of that model
        :param model: model to get object off
        :returns: random object of model
        """
        return TestDB.random_object(model)

    def test_apps(self):
        """ Tests for the apps.py of this module """
        from importlib import import_module
        module_title = self.__module__.split('.')[0]
        module = import_module(module_title + '.apps')
        class_ = getattr(module, module_title.title() + 'Config')
        self.assertEqual(class_.__name__, module_title.title() + 'Config')
