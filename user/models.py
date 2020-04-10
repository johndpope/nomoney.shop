from django.db import models
from django.contrib.auth.models import AbstractUser


class Calculator:
    """
    Levels:
        0 - No Deal match
        1 - One side Match
        2 - Two side Match
        3 - Deal between three users
        4 - Deal between four users

    users represent all users taking part at this deal
    """
    def __init__(self, me_, users):
        self.me_ = me_
        self.users = users  # users to deal with
        self._dealsets = set()  # cached

    def get_dealsets(self, level=None):
        if not self._dealsets:
            for user in self.users:
                self._dealsets.add(DealSet(self.me_, user))
        #self.me_.level1()
        self.me_.pulls[0].level2()
        #[self._dealsets.add(ds) for ds in self.create_level3_dealsets()]
        dealsets = self._dealsets
        if level == 1:
            dealsets = {ds for ds in self._dealsets if ds.level == 1}
        elif level == 2:
            dealsets = {ds for ds in self._dealsets if ds.level == 2}
        elif level == 3:
            dealsets = {ds for ds in self._dealsets if ds.level == 3}
        return dealsets

    def create_level3_dealsets(self):
        dealsets = set()
        for pull in self.me_.pulls:
            for action in pull.actions():
                user = action.user
                dealsets.add(action)
        print(dealsets)
        return dealsets

    def level1(self):
        """ One side exchange possibilities
        Added this to give the chance to find another item to change
        """
        listings = set()
        for listing in self.me_.listings:
            for action in listing.level1():
                listings.add(action)
        dealsets = set()
        for listing in listings:
            dealsets.add(DealSet(self.me_, listing.user))
        return dealsets  # self.get_dealsets(level=1)

    def level2(self):
        return self.get_dealsets(level=2)

    def level3(self):
        return self.get_dealsets(level=3)


class DealSet:
    def __init__(self, me_, users):
        self.me_ = me_
        self.users = [users] if isinstance(users, User) else users
        self.level = 0
        self.deals = self.get_deals()

    def get_deals(self):
        """ Calculate all deal constellations """
        deals = set()
        for user in self.users:
            deals.add(Deal(self.me_, user))
        if len(self.users) >= 2:
            pass
        for deal in deals:
            if deal.level:
                self.level = deal.level
        return deals


class Deal:
    """ These deals are for only two persons, ever!
    So level3 and up needs multiple Deals
    """
    def __init__(self, me_, user):
        self.me_ = me_
        self.user = user
        self.pushs = self.get_matching_pushs()  # push to that user
        self.pulls = self.get_matching_pulls()  # pull from that user
        self.level = self.set_level()

    def get_matching_pushs(self):
        return [push for push in self.user.pulls if push in self.me_.pushs]

    def get_matching_pulls(self):
        return [pull for pull in self.user.pushs if pull in self.me_.pulls]

    def set_level(self):
        level = 0
        if self.pushs and self.pulls:
            level = 2
        elif self.pushs or self.pulls:
            level = 1
        return level

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} vs. {}'.format(self.me_, self.user)


class User(AbstractUser):

    @property
    def listings(self):
        return self.listing_set.all()

    @property
    def other_users(self):
        return User.objects.all().exclude(pk=self.pk)

    @property
    def pushs(self):
        return self.listing_set.filter(type='push')

    @property
    def pulls(self):
        return self.listing_set.filter(type='pull')

    @property
    def calculator(self):
        return Calculator(self, self.other_users)

    #===========================================================================
    # def __hash__(self):
    #     return hash(self.username)
    #===========================================================================


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    score = models.PositiveSmallIntegerField()
    subject = models.CharField(max_length=100)
    text = models.TextField()
