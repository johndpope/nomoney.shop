from django.test import TestCase
from testdb import TestDB
from .models import Listing


class UserTestCase(TestCase):
    def setUp(self):
        TestDB.setup()

    def test_user_db(self):
        self.assertIs(len(Listing.objects.all()), TestDB.LISTING_COUNT)
