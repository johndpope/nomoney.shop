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
        self._deals = None  # cached

    def deals(self):
        if not self._deals:
            self._deals = [Deal(self.me_, user) for user in self.users]
        return self._deals

    def level1(self):
        """ One side exchange possibilities
        Added this to give the chance to find another item to change
        """
        return [deal for deal in self.deals() if deal.level == 1]

    def level2(self):
        return [deal for deal in self.deals() if deal.level == 2]


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


class User(AbstractUser):
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


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    score = models.PositiveSmallIntegerField()
    subject = models.CharField(max_length=100)
    text = models.TextField()
