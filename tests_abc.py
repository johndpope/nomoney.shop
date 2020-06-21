""" Abstract TestCase for all app tests """
from abc import ABC
from django.test import TestCase as BaseTestCase
from django.test import Client as BaseClient
from testdb import TestDB
from django.urls.base import reverse


class Client(BaseClient):
    def __init__(self, *args, **kwargs):
        BaseClient.__init__(self, *args, **kwargs)

    def get_name(self, url_name, *args, data=None, **extra):
        url = reverse(url_name, args=args)
        return BaseClient.get(self, url, data=data, **extra)

    def post_name(self, url_name, *args, data=None, **extra):
        url = reverse(url_name, args=args)
        return BaseClient.post(self, url, data=data**extra)


class TestCase(ABC, BaseTestCase):
    """ inherit this class for all tests """

    def run(self, *args, **kwargs):  # pylint: disable=arguments-differ
        response = None
        if self.__module__ != 'tests_abc':
            response = super().run(*args, **kwargs)
        return response

    def setUp(self):
        self.testdb = TestDB
        TestDB.setup()
        self.user = Client()
        self.user.login(
            username=self.testdb.USER_NAME,
            password=self.testdb.USER_PASSWORD,
            )
        self.anon = Client()

    def test_apps(self):
        """ Tests for the apps.py of this module """
        from importlib import import_module
        module_title = self.__module__.split('.')[0]
        module = import_module(module_title + '.apps')
        class_ = getattr(module, module_title.title() + 'Config')
        self.assertEqual(class_.__name__, module_title.title() + 'Config')
