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
        if isinstance(users, str):
            self.users = [users]  # users to deal with
        else:
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
    """ These deals are only two persons, ever!
    So level3 and up needs multiple Deals
    """
    def __init__(self, me_, user):
        self.me_ = me_
        self.user = user
        self.pushs = self.get_matching_pushs()  # push from that user
        self.pulls = self.get_matching_pulls()  # pull to that user
        self.level = self.set_level()

    def get_matching_pushs(self):
        return [push for push in self.me_.pushs if push in self.user.pulls]

    def get_matching_pulls(self):
        return [pull for pull in self.me_.pulls if pull in self.user.pushs]

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
    def pulls(self):
        return self.pull_set.all()

    @property
    def pushs(self):
        return self.push_set.all()

    @property
    def calculator(self):
        return Calculator(self, self.other_users)
    #[Deal(self, user) for user in self.other_users]


    #===========================================================================
    # @property
    # def first_level(self):
    #     """ Direct exchange possibilities """
    #     for user in self.other_users:
    #         #print(self.pushs, user.pulls)
    #         #pushs = [push for push in self.pushs if push in user.pulls]
    #         #print(self.pulls, user.pushs)
    #         #pulls = [pull for pull in self.pulls if pull in user.pushs]
    #         pushs = []
    #         for push in self.pushs:
    #             if push in user.pulls:
    #                 pushs.append(push)
    #         
    #         pulls = []
    #         for pull in self.pulls:
    #             if pull in user.pushs:
    #                 pulls.append(pull)
    #         
    #         if pushs and pulls:
    #             print(pushs, pulls)
    #             return {'pushs': pushs, 'pulls': pulls}
    #===========================================================================


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    score = models.PositiveSmallIntegerField()
    subject = models.CharField(max_length=100)
    text = models.TextField()
