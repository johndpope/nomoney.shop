""" Creation of a demo database also for testing purposes

To fill your development database with these sample data, do:
python manage.py shell
from testdb import TestDB
TestDB.setup()
"""
from random import randint
from user.models import User
from listing.models import Unit, Listing, Category


class TestDB:
    """ Management class for creating the database
    Install complete test/demo database with:
    from test_db import TestDB
    TestDB.setup()

    It's possible to install app specific databases if necessary:
    TestDB.setup_appname_db()
    """
    USER_COUNT = 10
    LISTING_COUNT = 100
    CATEGORIES = ['Apples', 'Bananas', 'Raspberrys', 'Bread', 'Water']
    UNITS = ['kg', 'g', 'pcs', 'litres']

    @classmethod
    def setup(cls):
        """ Setup complete test/demo database """
        cls.setup_user_db()
        cls.setup_listing_db()

    @classmethod
    def setup_user_db(cls):
        """ Setup User database only """
        for i in range(cls.USER_COUNT):
            i = str(i + 1)
            User.objects.create(
                username='test' + i,
                first_name='first' + i,
                last_name='last' + i,
                email='test{}@local.local'.format(i),
                )

    @classmethod
    def setup_listing_db(cls):
        """ Setup Listing database with all related models
        (Category and Unit)
        """
        cls._setup_listing_category_db()
        cls._setup_listing_unit_db()
        for i in range(cls.LISTING_COUNT):
            i = str(i + 1)
            type_ = ('push', 'pull')[randint(0, 1)]
            user = User.objects.all()[randint(0, cls.USER_COUNT - 1)]
            category = Category.objects.get(
                title=cls.CATEGORIES[randint(0, len(cls.CATEGORIES) - 1)]
                )
            count = randint(1, 1000)
            unit = Unit.objects.all()[randint(0, len(cls.UNITS) - 1)]
            title = '{} {}{}'.format(category.title, count, unit)
            Listing.objects.create(
                user=user,
                type=type_,
                unit=unit,
                title=title,
                count=count,
                category=category
                )

    @classmethod
    def _setup_listing_category_db(cls):
        parent = Category.objects.create(title='food')
        for category in cls.CATEGORIES:
            Category.objects.create(title=category, parent=parent)

    @classmethod
    def _setup_listing_unit_db(cls):
        """ must be run before listing db """
        for unit in cls.UNITS:
            Unit.objects.create(title=unit)
