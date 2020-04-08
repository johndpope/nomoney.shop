""" Abstract TestCase for all app tests """
from abc import ABC
from django.test import TestCase as BaseTestCase
from testdb import TestDB


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

    def test_apps(self):
        """ Tests for the apps.py of this module """
        from importlib import import_module
        module_title = self.__module__.split('.')[0]
        module = import_module(module_title + '.apps')
        class_ = getattr(module, module_title.title() + 'Config')
        self.assertEqual(class_.__name__, module_title.title() + 'Config')
