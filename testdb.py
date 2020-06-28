""" Creation of a demo database also for testing purposes

To fill your development database with these sample data, do:
python manage.py shell
from testdb import TestDB;TestDB.setup()

Oneline:
python manage.py shell -c "from testdb import TestDB;TestDB.setup()"
"""
from random import randint
from user.models import User
from listing.models import Unit, Push, Pull
from category.models import Category
from deal.models import Deal


class TestDB:
    """ Management class for creating the database
    Install complete test/demo database with (needs working empty database):
    from testdb import TestDB
    TestDB.setup()

    It's possible to install app specific databases if necessary:
    TestDB.setup_appname_db()
    """
    PRINT_STEPS = True
    USER_NAME = 'demo'
    USER_PASSWORD = 'demo123'
    USER_COUNT = 10
    LISTING_COUNT = 100
    DEAL_COUNT = 1
    CATEGORIES = {
        'Lebensmittel': ['Äpfel', 'Bananen', 'Erdbeeren', 'Brot', 'Wasser',
                         'Mehl', 'Eier', 'Pepperoni', 'Tomaten', 'Kopfsalat'],
        'Dienstleistung': ['Rasenmähen', 'Heckenschnitt', 'IT-Service', ]
        }

    UNITS = [
        ('Kilogramm', 'kg'),
        ('Gramm', 'g'),
        ('Stück', 'stk'),
        ('Liter', 'l'),
        ('Milliiter', 'ml'),
        ]

    TITLE_SUFFIX = [
        'frisch', 'frische Ernte', 'beschte', 'Original', 'Super Qualität',
        'erntefrisch', 'hervorragende Qualität'
        ]

    @classmethod
    def setup(cls):
        """ Setup complete test/demo database """
        cls.setup_user_db()
        cls.setup_unit_db()
        cls.setup_category_db()
        cls.setup_listing_db()
        cls.setup_deal_db()

    @classmethod
    def setup_user_db(cls):
        """ Setup User database only """
        user = User.objects.create(username=TestDB.USER_NAME)
        user.set_password(TestDB.USER_PASSWORD)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        for i in range(cls.USER_COUNT):
            key = str(i + 1)
            User.objects.create(
                username='test' + key,
                first_name='first' + key,
                last_name='last' + key,
                email='test{}@local.local'.format(key),
                )
            if not i % 10 and cls.PRINT_STEPS and i != 0:
                print(str(i) + ' users created.')

    @classmethod
    def setup_unit_db(cls):
        for title, short in cls.UNITS:
            Unit.objects.create(title=title, short=short)

    @classmethod
    def setup_category_db(cls):
        for category_str, sub_categories in cls.CATEGORIES.items():
            category = Category.objects.create(title=category_str)
            for sub_cat in sub_categories:
                Category.objects.create(parent=category, title=sub_cat)

    @classmethod
    def setup_listing_db(cls):
        """ Setup Listing database with all related models
        (Category and Unit)
        """
        for i in range(cls.LISTING_COUNT):
            listing_class = (Push, Pull)[randint(0, 1)]
            category = cls.random_object(Category)
            user = cls.random_object(User)
            quantity = randint(1, 2147483647)
            unit = cls.random_object(Unit)
            title = category.title + ' ' + \
                TestDB.TITLE_SUFFIX[randint(0, len(TestDB.TITLE_SUFFIX)-1)]

            listing_class.objects.create(
                category=category,
                user=user,
                title=title,
                quantity=quantity,
                unit=unit
                )
            if not i % 100 and cls.PRINT_STEPS and i != 0:
                print(str(i) + ' listings created.')

    @classmethod
    def setup_deal_db(cls):
        for i in range(cls.DEAL_COUNT):
            Deal.objects.create(
                user1=cls.random_object(User),
                user2=cls.random_object(User)
                )
            if not i % 100 and cls.PRINT_STEPS and i != 0:
                print(str(i) + ' deals created.')

    @staticmethod
    def random_object(model):
        objects = model.objects.all()
        return objects[randint(0, len(objects)-1)]
