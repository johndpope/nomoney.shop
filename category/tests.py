from tests_abc import TestCase
from django.db.models.query import QuerySet
from .models import Category


class CategoryTestCase(TestCase):
    def test_list_view(self):
        self.anon.get302('user_list')
        category = Category.objects.first()
        self.user.post302('category_create', data={'title': 'bla'})
        #self.user.post302('category_update', url_args=str(category.pk), data={'title': 'bla'})

    def test_models(self):
        category = Category.objects.latest()
        category1 = Category.objects.first()
        self.assertIsInstance(category, Category)
        self.assertIsInstance(category.pushs, QuerySet)
        self.assertIsInstance(category.pulls, QuerySet)
        self.assertIsInstance(category.listings, list)
        self.assertIsInstance(category.path, str)
        self.assertIsInstance(str(category), str)
        self.assertIs(len(category.listings) < len(category1.listings),
                      category < category1)
        self.assertIsInstance(category.count_pushs, int)
        self.assertIsInstance(category.count_pulls, int)
