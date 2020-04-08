from django.test import TestCase
from test_db import Test_db
from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        Test_db.setup()

    def test_user_db(self):
        self.assertIs(len(User.objects.all()), Test_db.USER_COUNT)
