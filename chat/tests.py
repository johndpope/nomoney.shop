from django.test import TestCase
from testdb import TestDB


class UserTestCase(TestCase):
    def setUp(self):
        TestDB.setup()

    def test_apps(self):
        """ Tests for the apps.py of this module """
        from importlib import import_module
        module_title = self.__module__.split('.')[0]
        module = import_module(module_title + '.apps')
        class_ = getattr(module, module_title.title() + 'Config')
        self.assertEqual(class_.__name__, module_title.title() + 'Config')
