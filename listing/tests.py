from tests_abc import TestCase
from .models import Push, Pull, Category
from django.db.models.query import QuerySet


class UserTestCase(TestCase):

    def test_user_db(self):
        self.assertEqual(
            len(Push.objects.all()) + len(Pull.objects.all()),
            self.testdb.LISTING_COUNT
            )


class CategoryTestCase(TestCase):

    def test_category_db(self):
        category = None
        for category in Category.objects.all():
            if category.parent:
                break
        pushs = category.pushs
        pulls = category.pulls
        self.assertIsInstance(pushs, QuerySet)
        self.assertIsInstance(pulls, QuerySet)
        self.assertIsInstance(category.path, str)
        self.assertIn('/', str(category))
