from django.db import models
from config.settings import AUTH_USER_MODEL
from .base import DealBase, DealSetBase


class DealSet(DealSetBase, models.Model):
    users = models.ManyToManyField(AUTH_USER_MODEL)
    is_virtual = False
    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        self.deal_class = Deal

    def get_users(self):
        return self.users.all()  # pylint: disable=no-member

    def set_users(self, *users):
        self.users.set(users)

    @property
    def deals(self):
        return self.deal_set.all()


class Deal(DealBase, models.Model):
    dealset = models.ForeignKey('deal.DealSet', on_delete=models.CASCADE)
    users = models.ManyToManyField(AUTH_USER_MODEL)
    accepted = models.BooleanField(default=False)
    is_virtual = False

    @property
    def user(self):
        return self._user or self.users.all()[0]

    @user.setter
    def user(self, value):
        self._user = value

    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)

    def get_users(self):
        return self.users.all()

    @property
    def bids(self):
        return self.bid_set.all()


#===============================================================================
# def dealset_users_changed(sender, **kwargs):
#     print(sender)
#     dealset = kwargs.get('instance')
#     users = User.objects.filter(pk__in=kwargs.get('pk_set'))
#     dealset.get_or_create_deals(users)
# 
# 
# m2m_changed.connect(dealset_users_changed, sender=DealSet.users.through)
#===============================================================================
