from django.db import models
from django.contrib.auth.models import AbstractUser
from listing.models import Listing


class DealSet:
    """
    Levels:
        0 - No Deal match
        1 - One side Match
        2 - Two side Match
        3 - Deal between three users
        4 - Deal between four users

    users represent all users taking part at this deal
    """
    def __init__(self, me_, user, middle=None):
        self.me_ = me_
        self.user = user
        self.middle = middle
        self.level = 0
        self.first_deal = None
        self.second_deal = None
        self.get_deals()

    def get_deals(self):
        """ Calculate all deal constellations """
        deals = set()
        if self.middle:
            self.first_deal = Deal(self.me_, self.middle)
            self.second_deal = Deal(self.me_, self.user)
            self.level = 3
        else:
            self.first_deal = Deal(self.me_, self.user)
            if self.first_deal.level:
                self.level = self.first_deal.level
        return deals


class Deal:
    """ These deals are for only two persons, ever!
    So level3 and up needs multiple Deals
    """
    def __init__(self, me_, user):
        self.me_ = me_
        self.user = user
        self.pushs = self._get_matching_pushs()  # push to that user
        self.pulls = self._get_matching_pulls()  # pull from that user
        self.level = self._set_level()

    def _get_matching_pushs(self):
        return [push for push in self.user.pulls if push in self.me_.pushs]

    def _get_matching_pulls(self):
        return [pull for pull in self.user.pushs if pull in self.me_.pulls]

    def _set_level(self):
        level = 0
        if self.pushs and self.pulls:
            level = 2
        elif self.pushs or self.pulls:
            level = 1
        return level

    def __repr__(self):
        return 'Deal: ' + str(self)

    def __str__(self):
        return '{} vs. {}'.format(self.me_, self.user)


class User(AbstractUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_listings = Listing.objects.all()
        self.listings = self.listing_set.all()
        self.other_users = User.objects.all().exclude(pk=self.pk)
        #self._level1 = set()
        #self._level2 = set()

    def actions(self, type_=None, reverse=False):
        """ all possible actions with self.listings """
        result = None
        if type_ and not reverse:  # return all own listings of same type
            result = self.listings.filter(type=type_)
        elif type_ and reverse:  # return all own listings of other type
            result = self.listings.exclude(type=type_)
        else:  # return all own listings
            result = self.listings
        return result

    def matches(self):
        users = set()
        for listing in self.listings:
            for user in {x.user for x in listing.matches()}:
                users.add(user)
        return users

    def find_dealers(self, pushs, pulls):
        users = {pull.user for pull in self.all_listings.filter(category__in=[push.category for push in pushs], type='pull')}
        dealers = set()
        for user in users:
            if user.pulls.filter(category__in=[pull.category for pull in pulls]):
                dealers.add(user)
        return dealers
            
    @property
    def pushs(self):
        return self.actions(type_='push')

    @property
    def pulls(self):
        return self.actions(type_='pull')

    def calculate(self, level_1_2):
        dealsets = set()
        for user in self.matches():
            dealset = DealSet(self, user)
            if dealset.level == level_1_2:
                dealsets.add(dealset)
        return dealsets

    def level1(self):
        return self.calculate(1)

    def level2(self):
        return self.calculate(2)

    def level3(self):
        level1 = self.level1()
        level3 = set()
        for dealset in level1:
            deal = dealset.first_deal
            if not deal.pushs:
                middle = self.find_dealers(self.pushs, deal.user.pulls)
                # suche listings pulls=self.pushs, pushs=deal.user.pulls
                for user in middle:
                    level3.add(DealSet(self, deal.user, middle=user))
            elif not deal.pulls:
                pass
        return level3

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    score = models.PositiveSmallIntegerField()
    subject = models.CharField(max_length=100)
    text = models.TextField()
