from tests_abc import TestCase
from testdb import TestDB
from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.all()[0]
        #=======================================================================
        # for user in User.objects.all():
        #     calc = user.calculator
        #     if calc.level1() and calc.level2():
        #         self.user = user
        #=======================================================================

    def test_user_db(self):
        self.assertIs(len(User.objects.all()), TestDB.USER_COUNT)

    def test_user_model(self):
        self.assertIs(len(self.user.matches()), len(User.objects.all()) - 1)
