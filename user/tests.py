from django.test import TestCase
from testdb import TestDB
from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        TestDB.setup()

    def test_user_db(self):
        self.assertIs(len(User.objects.all()), TestDB.USER_COUNT)
