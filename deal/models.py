from django.db import models
from django.db.models import Q
from config.settings import AUTH_USER_MODEL

class Deal(models.Model):
    user1 = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user1_deals'
        )
    user2 = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user2_deals'
        )
    guild = models.ForeignKey(
        'guild.Guild', on_delete=models.CASCADE, null=True, blank=True
        )
    accepted = models.BooleanField(default=False)

    pov_user = None

    @property
    def user(self):
        if self.pov_user == self.user2:
            return self.user2
        return self.user1

    @property
    def partner(self):
        if self.pov_user == self.user2:
            return self.user1
        return self.user2

    @property
    def bids(self):
        return self.bid_set.all()

    @property
    def pushs(self):
        # pylint: disable=no-member
        return list(self.intersection(self.user.pushs, self.partner.pulls))

    @property
    def pulls(self):
        # pylint: disable=no-member
        return list(self.intersection(self.user.pulls, self.partner.pushs))

    @staticmethod
    def intersection(lst1, lst2):
        """ returns intersecting elements """
        for element in lst1:
            if element in lst2:
                yield element

    def set_pov(self, me_):
        self.pov_user = me_

    def get_users(self):
        return self.user1, self.user2

    def get_latest_bid(self):
        bids = self.bids
        return bids.latest() if bids else None

    #===========================================================================
    # def bid_allowed_for(self):
    #     if self.accepted:
    #         return []
    #     latest_bid = self.get_latest_bid()
    #     if latest_bid:
    #         userlist = list(self.get_users())
    #         userlist.remove(self.bids.latest().creator)
    #         return userlist
    #     return self.get_users()
    #===========================================================================

    def can_accept(self, user):
        latest_bid = self.get_latest_bid()
        if not latest_bid:
            return False
        if latest_bid.creator != user:
            return True
        return False

        import pdb; pdb.set_trace()  # <---------

    def can_bid(self, user):
        latest_bid = self.get_latest_bid()
        if not latest_bid:
            return True
        if latest_bid.creator != user:
            return True
        return False




    #===========================================================================
    # def save(self, *args, **kwargs):
    #     existing = self.__class__.objects.filter(
    #         Q(user1=self.user1, user2=self.user2) | \
    #         Q(user2=self.user1, user1=self.user2)
    #         ).exclude(accepted=True)
    #     if existing:
    #         raise AttributeError('Object exists')
    #     return models.Model.save(self, *args, **kwargs)
    #===========================================================================
