from tests_abc import TestCase
from testdb import TestDB
from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        super().setUp()
        for user in User.objects.all():
            calc = user.calculator
            if calc.level1() and calc.level2():
                self.user = user

    def test_user_db(self):
        self.assertIs(len(User.objects.all()), TestDB.USER_COUNT)

    def test_user_model(self):
        calculator = self.user.calculator
        # Need rework:
        self.assertIs(len(calculator.deals()), len(User.objects.all()) - 1)

        self.assertIsInstance(calculator.level1(), list)
        self.assertIsInstance(calculator.level2(), list)

