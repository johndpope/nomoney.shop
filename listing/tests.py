""" tests for the listing module """
from django.db.models.query import QuerySet
from tests_abc import TestCase
from category.models import Category
from .models import Push, Pull, Unit


class ListingTestCase(TestCase):
    """ tests for the listing module """

    def test_user_db(self):
        """ tests for the listing module with user database parts """
        self.assertEqual(
            len(Push.objects.all()) + len(Pull.objects.all()),
            self.testdb.LISTING_COUNT
            )

    def test_category_db(self):
        """ test category related parts """
        category = None
        for category in Category.objects.all():
            if category.parent:
                break
        pushs = category.pushs
        pulls = category.pulls
        self.assertIsInstance(pushs, QuerySet)
        self.assertIsInstance(pulls, QuerySet)
        self.assertIsInstance(category.path, str)

    def test_listing_form(self):
        """ test listing form parts """
        url = 'listing_create'
        data = {
            'title': 'testtitle',
            'quantity': '4',
            'unit': Unit.objects.first().pk,
            'category': Category.objects.first().pk
            }
        listing = Push.objects.first()
        self.user.getpost(url, url_args='pull', data=data)
        self.user.getpost(url, url_args='push', data=data)
        self.anon.post302(url, url_args='pull', data=data)
        self.anon.post302(url, url_args='push', data=data)

        url = 'category_listing_create'
        url_args = ('pull', listing.pk)
        self.user.getpost(url, url_args=url_args, data=data)
        self.anon.get302(url, url_args=url_args)

        url_args = ('push', listing.pk)
        self.user.getpost(url, url_args=url_args, data=data)
        self.anon.get302(url, url_args=url_args)
