from itertools import combinations
from django.db import models
from django.db.models.signals import m2m_changed
from config.settings import AUTH_USER_MODEL
from user.models import User


class DealSet(models.Model):
    users = models.ManyToManyField(AUTH_USER_MODEL)

    @property
    def deals(self):
        return self.get_or_create_deals(self.users)

    @property
    def pushs(self):
        push_qs = [user.pushs for user in self.users.all()]
        return push_qs[0].union(*push_qs)

    @property
    def pulls(self):
        pull_qs = [user.pulls for user in self.users.all()]
        return pull_qs[0].union(*pull_qs)

    def get_or_create_deals(self, users, pov_user=None):
        if not self.deal_set.all():
            for user_combi in combinations(users, 2):
                deal = Deal.objects.create(dealset=self)
                deal.set_pov(pov_user)
                deal.users.set(user_combi)
                deal.save()
        return self.deal_set.all()

    def set_pov(self, user):
        self.get_or_create_deals(self.users, pov_user=user)

    @classmethod
    def by_users(cls, users):
        import pdb; pdb.set_trace()  # <---------


def dealset_users_changed(sender, **kwargs):
    print(sender)
    dealset = kwargs.get('instance')
    users = User.objects.filter(pk__in=kwargs.get('pk_set'))
    dealset.get_or_create_deals(users)


m2m_changed.connect(dealset_users_changed, sender=DealSet.users.through)


class Deal(models.Model):
    dealset = models.ForeignKey('deal.DealSet', on_delete=models.CASCADE)
    users = models.ManyToManyField(AUTH_USER_MODEL)
    accepted = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.user = self.users.all()[0]
        except ValueError as _:
            pass

    @property
    def partner(self):
        if self.user:
            for user in self.users.all():
                if user != self.user:
                    return user
        else:
            raise AttributeError("Cannot get partner without knowing user")

    @property
    def bids(self):
        return self.bid_set.all()

    @property
    def pushs(self):
        return list(self.intersection(self.user.pushs, self.partner.pulls))

    @property
    def pulls(self):
        return list(self.intersection(self.user.pulls, self.partner.pushs))

    def set_pov(self, user):
        if user in self.users.all():
            self.user = user

    @staticmethod
    def intersection(lst1, lst2):
        """ returns intersecting elements """
        for element in lst1:
            if element in lst2:
                yield element
    @classmethod
    def by_users(cls, users):
        import pdb; pdb.set_trace()  # <---------
