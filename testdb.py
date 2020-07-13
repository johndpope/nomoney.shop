""" Creation of a demo database also for testing purposes

To fill your development database with these sample data, do:
python manage.py shell
from testdb import TestDB;TestDB.setup()

Oneline:
python manage.py shell -c "from testdb import TestDB;TestDB.setup()"
"""
from random import randint
from lorem import get_sentence, get_word
from names import get_first_name, get_last_name
from user.models import User
from listing.models import Unit, Push, Pull
from category.models import Category
from deal.models import Deal
from location.models import Location
from market.models import Market
from bid.models import Bid, BidPosition


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
    USER_COUNT = 100
    LISTING_COUNT = 1000
    DEAL_COUNT = 10
    LOCATION_COUNT = 100
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

    demo, demo1, deal, location, market = 5 * [None]

    @classmethod
    def setup(cls):
        """ Setup complete test/demo database """
        cls.setup_user_db()
        cls.setup_location_db()
        cls.setup_unit_db()
        cls.setup_category_db()
        cls.setup_listing_db()
        cls.setup_market_db()
        cls.setup_deal_db()
        cls.setup_bid_db()

    @classmethod
    def setup_user_db(cls):
        """ Setup User database only """
        cls.demo = User.objects.create(
            username=TestDB.USER_NAME,
            first_name=get_first_name(),
            last_name=get_last_name(),
            email='demo@nomoney.shop',
            description=cls.sentences_string(),
            test=True,
            )
        cls.demo.set_password(TestDB.USER_PASSWORD)
        cls.demo.is_superuser = True
        cls.demo.is_staff = True
        cls.demo.save()
        cls.demo1 = User.objects.create(
            username=TestDB.USER_NAME + '1',
            first_name=get_first_name(),
            last_name=get_last_name(),
            email='demo1@nomoney.shop',
            description=cls.sentences_string(),
            test=True,
            )
        cls.demo1.set_password(TestDB.USER_PASSWORD)
        cls.demo1.is_superuser = True
        cls.demo1.is_staff = True
        cls.demo1.save()
        for i in range(cls.USER_COUNT):
            key = str(i + 1)
            User.objects.create(
                username=get_first_name() + str(randint(0, 2000)),
                first_name=get_first_name(),
                last_name=get_last_name(),
                email='test{}@local.local'.format(key),
                description=cls.sentences_string(),
                test=True,
                )
            if cls.PRINT_STEPS and not i % 10 and i != 0:
                print(str(i) + ' users created.')

    @classmethod
    def setup_location_db(cls):
        cls.location = Location.objects.create(
            title='Demos Treffpunkt',
            user=cls.demo,
            lon=randint(-180, 180),
            lat=randint(-90, 90),
            description=cls.sentences_string(),
            test=True,
            )
        Location.objects.create(
            title='Demo1 Zuhause',
            user=cls.demo1,
            lon=randint(-180, 180),
            lat=randint(-90, 90),
            description=cls.sentences_string(),
            test=True,
            )
        for i in range(cls.LOCATION_COUNT):
            Location.objects.create(
                title=get_word()[0:20],
                user=cls.random_object(User),
                lon=randint(-180, 180),
                lat=randint(-90, 90),
                description=cls.sentences_string(),
                test=True,
                )
            if cls.PRINT_STEPS and not i % 100 and i != 0:
                print(str(i) + ' locations created.')

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
            quantity = randint(1, 5000)  # max 2147483647
            unit = cls.random_object(Unit)
            title = category.title + ' ' + \
                TestDB.TITLE_SUFFIX[randint(0, len(TestDB.TITLE_SUFFIX)-1)]
            listing_class.objects.create(
                category=category,
                user=user,
                title=title,
                quantity=quantity,
                unit=unit,
                description=cls.sentences_string(10),
                test=True,
                )
            if cls.PRINT_STEPS and not i % 100 and i != 0:
                print(str(i) + ' listings created.')

    @classmethod
    def setup_deal_db(cls):
        cls.deal = Deal.objects.create(user1=cls.demo, user2=cls.demo1)
        cls.deal = Deal.objects.create(
            user1=cls.demo, user2=cls.random_object(User)
            )
        Deal.objects.create(user1=cls.random_object(User), user2=cls.demo)
        Deal.objects.create(
            user1=cls.random_object(User), user2=cls.random_object(User)
            )
        for i in range(cls.DEAL_COUNT):
            Deal.objects.create(
                user1=cls.demo,
                user2=cls.random_object(User)
                )
            if cls.PRINT_STEPS and not i % 100 and i != 0:
                print(str(i) + ' deals created.')

    @classmethod
    def setup_bid_db(cls):
        """ create bid for a deal and accept """
        bid = Bid.objects.create(deal=cls.deal, creator=cls.demo)
        for push in bid.pushs:
            BidPosition.objects.create(
                push=push, bid=bid, quantity=randint(0, 100), unit=push.unit
                )
        for push in bid.pulls:
            BidPosition.objects.create(
                push=push, bid=bid, quantity=randint(0, 100), unit=push.unit
                )
        bid = Bid.objects.create(deal=cls.deal, creator=cls.deal.user2)
        for push in bid.pushs:
            BidPosition.objects.create(
                push=push, bid=bid, quantity=randint(0, 100), unit=push.unit
                )
        for push in bid.pulls:
            BidPosition.objects.create(
                push=push, bid=bid, quantity=randint(0, 100), unit=push.unit
                )

    @classmethod
    def setup_market_db(cls):
        """ create bid for a deal and accept """
        market = Market.objects.create(
            title=get_word()[0:20], location=cls.location, test=True,
            )
        market.users.add(cls.demo)
        market.users.add(cls.demo1)
        market.users.add(cls.random_object(User))
        market.save()

        market = Market.objects.create(
            title=get_word()[0:20], location=cls.location, test=True,
            )
        market.users.add(cls.demo)
        market.users.add(cls.demo1)
        market.users.add(cls.random_object(User))
        market.users.add(cls.random_object(User))
        market.save()

        market = Market.objects.create(
            title=get_word()[0:20], location=cls.location, test=True,
            )
        market.users.add(cls.demo)
        market.users.add(cls.demo1)
        market.users.add(cls.random_object(User))
        market.users.add(cls.random_object(User))
        market.users.add(cls.random_object(User))
        market.save()
        cls.market = market

        market = Market.objects.create(
            title=get_word()[0:20], location=cls.location, test=True,
            )
        market.users.add(cls.random_object(User))
        market.users.add(cls.random_object(User))
        market.users.add(cls.random_object(User))
        market.save()

    @classmethod
    def setup_feedback_db(cls):
        """ create feedback after bid accepted in previous step """
        pass

    @classmethod
    def setup_chat_db(cls):
        """ dont know what to test here """
        pass

    @staticmethod
    def sentences_string(runs=5):
        sentence = ''
        for _ in range(runs):
            sentence += get_sentence() + ' '
        return sentence

    @staticmethod
    def random_object(model):
        objects = model.objects.all()
        return objects[randint(0, len(objects)-1)]
