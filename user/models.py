from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    @property
    def other_users(self):
        return self.__class__.objects.exclude(pk=self.pk)

    @property
    def pushs(self):
        return self.push_set.all()

    @property
    def pulls(self):
        return self.pull_set.all()

    @property
    def listings(self):
        """ returns list of listings (pushs and pulls) """
        return list(self.pushs) + list(self.pulls)

    @property
    def bids(self):
        return sorted(
            {*self.bids_sent.all(), *self.bids_received.all()},
            key=lambda x: x.datetime
            )

    @property
    def deals(self):
        deals = self.user1_deals.all().union(self.user2_deals.all())
        for deal in deals:
            deal.set_pov(self)
        return deals
